    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> MembersFiles:
        ...

    @overload
    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> TypedAsyncResult[MembersFiles]:
        ...

    def get_members_files(
        self,
        member_ids: List[int],
        branch_ids: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[MembersFiles], MembersFiles, TypedAsyncResult[List[MembersFiles]], TypedAsyncResult[MembersFiles]]:
        """Get members files from one or multiple branches."""
        if not branch_ids and not self.branch_api_clients:
            # Use default client implementation
            members_files = MembersFiles(
                member_ids=member_ids,
                data_from=from_date,
                data_to=to_date
            )
            
            try:
                if async_req:
                    # Start all async requests for each member
                    async_results = []
                    for member_id in member_ids:
                        async_results.extend([
                            self.members_api.get_member_profile(id_member=member_id, async_req=True),
                            self.get_contracts(member_id=member_id, active_only=False, async_req=True),
                            self.entries_api.get_entries(
                                register_date_start=from_date,
                                register_date_end=to_date,
                                member_id=member_id,
                                async_req=True
                            ),
                            self.receivables_api.get_receivables(
                                member_id=member_id,
                                registration_date_start=from_date,
                                registration_date_end=to_date,
                                async_req=True
                            ),
                            self.activities_api.get_schedule(
                                member_id=member_id,
                                date=from_date,
                                show_full_week=True,
                                async_req=True
                            )
                        ])
                    
                    # Create async result that will process all data
                    async_result = create_async_result(
                        pool=self._pool,
                        callback=lambda _: self._process_members_files(
                            [r.get() for r in async_results],
                            member_ids,
                            members_files
                        ),
                        error_callback=lambda e: members_files
                    )
                    return cast(TypedAsyncResult[MembersFiles], async_result)
                
                # Synchronous execution
                all_results = []
                for member_id in member_ids:
                    all_results.extend([
                        self.members_api.get_member_profile(id_member=member_id, async_req=False),
                        self.get_contracts(member_id=member_id, active_only=False, async_req=False),
                        self.entries_api.get_entries(
                            register_date_start=from_date,
                            register_date_end=to_date,
                            member_id=member_id,
                            async_req=False
                        ),
                        self.receivables_api.get_receivables(
                            member_id=member_id,
                            registration_date_start=from_date,
                            registration_date_end=to_date,
                            async_req=False
                        ),
                        self.activities_api.get_schedule(
                            member_id=member_id,
                            date=from_date,
                            show_full_week=True,
                            async_req=False
                        )
                    ])
                return self._process_members_files(all_results, member_ids, members_files)
            except Exception as e:
                logger.error(f"Error fetching members files: {str(e)}")
                return members_files
        
        branch_ids = branch_ids or list(self.branch_api_clients.keys())
        results = []
        
        for branch_id in branch_ids:
            if branch_id in self.branch_api_clients:
                # Create temporary GymApi instance with branch client
                branch_api = GymApi(api_client=self.branch_api_clients[branch_id])
                result = branch_api.get_members_files(
                    member_ids=member_ids,
                    from_date=from_date,
                    to_date=to_date,
                    async_req=True  # Always async for parallel processing
                )
                results.append(result)
        
        if async_req:
            async_result = self._pool.map_async(lambda r: r.get() if isinstance(r, AsyncResult) else r, results)
            return cast(TypedAsyncResult[List[MembersFiles]], async_result)
        
        # Wait for all results
        members_files = [r.get() if isinstance(r, AsyncResult) else r for r in results]
        return members_files if len(members_files) > 1 else members_files[0]

    def _create_member_profile(self, member: Any) -> MemberProfile:
        """Create a member profile from API member data."""
        return MemberProfile(
            member_id=member.id_member,
            name=member.name or "",
            email=member.email,
            phone=member.phone,
            photo_url=member.photo_url
        )

    def _build_member_timeline(self, profile: MemberProfile) -> None:
        """Build a chronological timeline of member events."""
        # Add entries
        for entry in profile.entries_history:
            profile.add_timeline_event(
                event_type=MemberEventType.ENTRY,
                timestamp=entry.register_date,
                description=f"Gym entry - {entry.entry_type.value}",
                related_id=entry.id,
                branch_id=entry.branch_id,
                status=entry.status.value
            )
            
        # Add financial transactions
        for receivable in profile.receivables:
            # Payment made
            if receivable.receiving_date:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.receiving_date,
                    description=f"Payment received - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount_paid,
                    transaction_type="payment",
                    payment_method=receivable.payment_method if hasattr(receivable, 'payment_method') else None
                )
            
            # Payment due
            if receivable.status == ReceivableStatus.OVERDUE:
                profile.add_timeline_event(
                    event_type=MemberEventType.FINANCIAL,
                    timestamp=receivable.due_date or datetime.now(),
                    description=f"Payment overdue - {receivable.description}",
                    related_id=receivable.id,
                    amount=receivable.amount,
                    transaction_type="overdue",
                    status="overdue"
                )
            
        # Sort all events by timestamp
        profile.timeline.sort(key=lambda x: x.timestamp)

    def _process_members_files(
        self,
        results: List[Any],
        member_ids: List[int],
        members_files: MembersFiles
    ) -> MembersFiles:
        """Process async results into MembersFiles object."""
        try:
            # Results come in groups of 5 per member (member, contracts, entries, receivables, sessions)
            results_per_member = 5
            for i, member_id in enumerate(member_ids):
                base_idx = i * results_per_member
                member = results[base_idx]
                
                if member:
                    profile = self._create_member_profile(member)
                    
                    # Process contracts
                    contracts = results[base_idx + 1]
                    if contracts:
                        profile.contracts_history = contracts
                        active_contracts = [c for c in contracts if c.status == MembershipStatus.ACTIVE]
                        if active_contracts:
                            profile.current_contract = active_contracts[0]
                            profile.is_active = True
                    
                    # Process entries
                    entries = results[base_idx + 2]
                    if entries:
                        profile.entries_history = [self._convert_entry(e) for e in entries]
                        profile.total_entries = len(profile.entries_history)
                        if profile.entries_history:
                            profile.last_entry = profile.entries_history[-1]
                    
                    # Process receivables
                    receivables = results[base_idx + 3]
                    if receivables:
                        profile.receivables = [self._convert_receivable(r) for r in receivables]
                        # Calculate financial summaries
                        for receivable in profile.receivables:
                            if receivable.status == ReceivableStatus.PAID:
                                profile.total_paid += receivable.amount or Decimal('0.00')
                            elif receivable.status == ReceivableStatus.PENDING:
                                profile.pending_payments += receivable.amount or Decimal('0.00')
                            elif receivable.status == ReceivableStatus.OVERDUE:
                                profile.overdue_payments += receivable.amount or Decimal('0.00')
                    
                    # Process activity sessions
                    sessions = results[base_idx + 4]
                    if sessions:
                        profile.total_classes_attended = len(sessions)
                        activity_counts: Dict[str, int] = {}
                        for session in sessions:
                            activity_name = getattr(session, 'activity_name', None)
                            if activity_name:
                                activity_counts[activity_name] = activity_counts.get(activity_name, 0) + 1
                        profile.favorite_activities = sorted(
                            activity_counts.keys(),
                            key=lambda x: activity_counts[x],
                            reverse=True
                        )[:5]
                    
                    # Build timeline
                    self._build_member_timeline(profile)
                    
                    # Add profile to collection
                    members_files.add_member(profile)
            
        except Exception as e:
            logger.error(f"Error processing members files: {str(e)}")
            
        return members_files

    def _process_member_data(self, profile: MemberProfile, results: List[Any]) -> None:
        """Process member data from API results."""
        try:
            # Process receivables
            receivables = results[3] if len(results) > 3 else None
            if receivables:
                profile.receivables = [self._convert_receivable(r) for r in receivables]
                # Calculate financial summaries
                for receivable in profile.receivables:
                    if receivable.status == ReceivableStatus.PAID:
                        profile.total_paid += receivable.amount or Decimal('0.00')
                    elif receivable.status == ReceivableStatus.PENDING:
                        profile.pending_payments += receivable.amount or Decimal('0.00')
                    elif receivable.status == ReceivableStatus.OVERDUE:
                        profile.overdue_payments += receivable.amount or Decimal('0.00')

            # Build timeline after all data is processed
            self._build_member_timeline(profile)
        except Exception as e:
            logger.error(f"Error processing member data: {str(e)}")
            raise

    def _convert_entry(self, entry: Any) -> GymEntry:
        """Convert SDK entry model to our GymEntry model."""
        try:
            entry_type = EntryType.REGULAR
            if entry.entry_type:
                if entry.entry_type.lower() == "guest":
                    entry_type = EntryType.GUEST
                elif entry.entry_type.lower() == "trial":
                    entry_type = EntryType.TRIAL
                elif entry.entry_type.lower() == "event":
                    entry_type = EntryType.EVENT

            return GymEntry(
                idEntry=entry.id or 0,
                idMember=entry.id_member,
                idProspect=entry.id_prospect,
                registerDate=entry.date or datetime.now(),
                entryType=entry_type,
                status=EntryStatus.VALID,  # Default to valid since API doesn't provide status
                idBranch=entry.id_branch,
                idActivity=None,  # API doesn't provide activity info
                idMembership=None,  # API doesn't provide membership info
                deviceId=entry.device,
                notes=entry.block_reason
            )
        except Exception as e:
            logger.error(f"Error converting entry: {str(e)}")
            return GymEntry(
                idEntry=0,
                idMember=None,
                idProspect=None,
                registerDate=datetime.now(),
                entryType=EntryType.REGULAR,
                status=EntryStatus.INVALID,
                idBranch=None,
                idActivity=None,
                idMembership=None,
                deviceId=None,
                notes=None
            )
