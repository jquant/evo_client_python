# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SaleItensViewModel(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id_sale_item': 'int',
        'description': 'str',
        'item': 'str',
        'item_value': 'float',
        'sale_value': 'float',
        'sale_value_without_credit_value': 'float',
        'quantity': 'int',
        'id_membership': 'int',
        'id_membership_renewed': 'int',
        'num_members': 'int',
        'id_product': 'int',
        'id_service': 'int',
        'corporate_partnership_name': 'str',
        'coporate_partnership_id': 'int',
        'membership_start_date': 'datetime',
        'discount': 'float',
        'corporate_discount': 'float',
        'tax': 'float',
        'voucher': 'str',
        'accounting_code': 'str',
        'municipal_service_code': 'str',
        'fl_receipt_only': 'bool',
        'id_sale_item_migration': 'str',
        'fl_swimming': 'bool',
        'fl_allow_locker': 'bool',
        'id_member_membership': 'int',
        'value_next_month': 'float'
    }

    attribute_map = {
        'id_sale_item': 'idSaleItem',
        'description': 'description',
        'item': 'item',
        'item_value': 'itemValue',
        'sale_value': 'saleValue',
        'sale_value_without_credit_value': 'saleValueWithoutCreditValue',
        'quantity': 'quantity',
        'id_membership': 'idMembership',
        'id_membership_renewed': 'idMembershipRenewed',
        'num_members': 'numMembers',
        'id_product': 'idProduct',
        'id_service': 'idService',
        'corporate_partnership_name': 'corporatePartnershipName',
        'coporate_partnership_id': 'coporatePartnershipId',
        'membership_start_date': 'membershipStartDate',
        'discount': 'discount',
        'corporate_discount': 'corporateDiscount',
        'tax': 'tax',
        'voucher': 'voucher',
        'accounting_code': 'accountingCode',
        'municipal_service_code': 'municipalServiceCode',
        'fl_receipt_only': 'flReceiptOnly',
        'id_sale_item_migration': 'idSaleItemMigration',
        'fl_swimming': 'flSwimming',
        'fl_allow_locker': 'flAllowLocker',
        'id_member_membership': 'idMemberMembership',
        'value_next_month': 'valueNextMonth'
    }

    def __init__(self, id_sale_item=None, description=None, item=None, item_value=None, sale_value=None, sale_value_without_credit_value=None, quantity=None, id_membership=None, id_membership_renewed=None, num_members=None, id_product=None, id_service=None, corporate_partnership_name=None, coporate_partnership_id=None, membership_start_date=None, discount=None, corporate_discount=None, tax=None, voucher=None, accounting_code=None, municipal_service_code=None, fl_receipt_only=None, id_sale_item_migration=None, fl_swimming=None, fl_allow_locker=None, id_member_membership=None, value_next_month=None):  # noqa: E501
        """SaleItensViewModel - a model defined in Swagger"""  # noqa: E501
        self._id_sale_item = None
        self._description = None
        self._item = None
        self._item_value = None
        self._sale_value = None
        self._sale_value_without_credit_value = None
        self._quantity = None
        self._id_membership = None
        self._id_membership_renewed = None
        self._num_members = None
        self._id_product = None
        self._id_service = None
        self._corporate_partnership_name = None
        self._coporate_partnership_id = None
        self._membership_start_date = None
        self._discount = None
        self._corporate_discount = None
        self._tax = None
        self._voucher = None
        self._accounting_code = None
        self._municipal_service_code = None
        self._fl_receipt_only = None
        self._id_sale_item_migration = None
        self._fl_swimming = None
        self._fl_allow_locker = None
        self._id_member_membership = None
        self._value_next_month = None
        self.discriminator = None
        if id_sale_item is not None:
            self.id_sale_item = id_sale_item
        if description is not None:
            self.description = description
        if item is not None:
            self.item = item
        if item_value is not None:
            self.item_value = item_value
        if sale_value is not None:
            self.sale_value = sale_value
        if sale_value_without_credit_value is not None:
            self.sale_value_without_credit_value = sale_value_without_credit_value
        if quantity is not None:
            self.quantity = quantity
        if id_membership is not None:
            self.id_membership = id_membership
        if id_membership_renewed is not None:
            self.id_membership_renewed = id_membership_renewed
        if num_members is not None:
            self.num_members = num_members
        if id_product is not None:
            self.id_product = id_product
        if id_service is not None:
            self.id_service = id_service
        if corporate_partnership_name is not None:
            self.corporate_partnership_name = corporate_partnership_name
        if coporate_partnership_id is not None:
            self.coporate_partnership_id = coporate_partnership_id
        if membership_start_date is not None:
            self.membership_start_date = membership_start_date
        if discount is not None:
            self.discount = discount
        if corporate_discount is not None:
            self.corporate_discount = corporate_discount
        if tax is not None:
            self.tax = tax
        if voucher is not None:
            self.voucher = voucher
        if accounting_code is not None:
            self.accounting_code = accounting_code
        if municipal_service_code is not None:
            self.municipal_service_code = municipal_service_code
        if fl_receipt_only is not None:
            self.fl_receipt_only = fl_receipt_only
        if id_sale_item_migration is not None:
            self.id_sale_item_migration = id_sale_item_migration
        if fl_swimming is not None:
            self.fl_swimming = fl_swimming
        if fl_allow_locker is not None:
            self.fl_allow_locker = fl_allow_locker
        if id_member_membership is not None:
            self.id_member_membership = id_member_membership
        if value_next_month is not None:
            self.value_next_month = value_next_month

    @property
    def id_sale_item(self):
        """Gets the id_sale_item of this SaleItensViewModel.  # noqa: E501


        :return: The id_sale_item of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_sale_item

    @id_sale_item.setter
    def id_sale_item(self, id_sale_item):
        """Sets the id_sale_item of this SaleItensViewModel.


        :param id_sale_item: The id_sale_item of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_sale_item = id_sale_item

    @property
    def description(self):
        """Gets the description of this SaleItensViewModel.  # noqa: E501


        :return: The description of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SaleItensViewModel.


        :param description: The description of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def item(self):
        """Gets the item of this SaleItensViewModel.  # noqa: E501


        :return: The item of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this SaleItensViewModel.


        :param item: The item of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._item = item

    @property
    def item_value(self):
        """Gets the item_value of this SaleItensViewModel.  # noqa: E501


        :return: The item_value of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._item_value

    @item_value.setter
    def item_value(self, item_value):
        """Sets the item_value of this SaleItensViewModel.


        :param item_value: The item_value of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._item_value = item_value

    @property
    def sale_value(self):
        """Gets the sale_value of this SaleItensViewModel.  # noqa: E501


        :return: The sale_value of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._sale_value

    @sale_value.setter
    def sale_value(self, sale_value):
        """Sets the sale_value of this SaleItensViewModel.


        :param sale_value: The sale_value of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._sale_value = sale_value

    @property
    def sale_value_without_credit_value(self):
        """Gets the sale_value_without_credit_value of this SaleItensViewModel.  # noqa: E501


        :return: The sale_value_without_credit_value of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._sale_value_without_credit_value

    @sale_value_without_credit_value.setter
    def sale_value_without_credit_value(self, sale_value_without_credit_value):
        """Sets the sale_value_without_credit_value of this SaleItensViewModel.


        :param sale_value_without_credit_value: The sale_value_without_credit_value of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._sale_value_without_credit_value = sale_value_without_credit_value

    @property
    def quantity(self):
        """Gets the quantity of this SaleItensViewModel.  # noqa: E501


        :return: The quantity of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this SaleItensViewModel.


        :param quantity: The quantity of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def id_membership(self):
        """Gets the id_membership of this SaleItensViewModel.  # noqa: E501


        :return: The id_membership of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_membership

    @id_membership.setter
    def id_membership(self, id_membership):
        """Sets the id_membership of this SaleItensViewModel.


        :param id_membership: The id_membership of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_membership = id_membership

    @property
    def id_membership_renewed(self):
        """Gets the id_membership_renewed of this SaleItensViewModel.  # noqa: E501


        :return: The id_membership_renewed of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_membership_renewed

    @id_membership_renewed.setter
    def id_membership_renewed(self, id_membership_renewed):
        """Sets the id_membership_renewed of this SaleItensViewModel.


        :param id_membership_renewed: The id_membership_renewed of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_membership_renewed = id_membership_renewed

    @property
    def num_members(self):
        """Gets the num_members of this SaleItensViewModel.  # noqa: E501


        :return: The num_members of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._num_members

    @num_members.setter
    def num_members(self, num_members):
        """Sets the num_members of this SaleItensViewModel.


        :param num_members: The num_members of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._num_members = num_members

    @property
    def id_product(self):
        """Gets the id_product of this SaleItensViewModel.  # noqa: E501


        :return: The id_product of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_product

    @id_product.setter
    def id_product(self, id_product):
        """Sets the id_product of this SaleItensViewModel.


        :param id_product: The id_product of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_product = id_product

    @property
    def id_service(self):
        """Gets the id_service of this SaleItensViewModel.  # noqa: E501


        :return: The id_service of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_service

    @id_service.setter
    def id_service(self, id_service):
        """Sets the id_service of this SaleItensViewModel.


        :param id_service: The id_service of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_service = id_service

    @property
    def corporate_partnership_name(self):
        """Gets the corporate_partnership_name of this SaleItensViewModel.  # noqa: E501


        :return: The corporate_partnership_name of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._corporate_partnership_name

    @corporate_partnership_name.setter
    def corporate_partnership_name(self, corporate_partnership_name):
        """Sets the corporate_partnership_name of this SaleItensViewModel.


        :param corporate_partnership_name: The corporate_partnership_name of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._corporate_partnership_name = corporate_partnership_name

    @property
    def coporate_partnership_id(self):
        """Gets the coporate_partnership_id of this SaleItensViewModel.  # noqa: E501


        :return: The coporate_partnership_id of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._coporate_partnership_id

    @coporate_partnership_id.setter
    def coporate_partnership_id(self, coporate_partnership_id):
        """Sets the coporate_partnership_id of this SaleItensViewModel.


        :param coporate_partnership_id: The coporate_partnership_id of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._coporate_partnership_id = coporate_partnership_id

    @property
    def membership_start_date(self):
        """Gets the membership_start_date of this SaleItensViewModel.  # noqa: E501


        :return: The membership_start_date of this SaleItensViewModel.  # noqa: E501
        :rtype: datetime
        """
        return self._membership_start_date

    @membership_start_date.setter
    def membership_start_date(self, membership_start_date):
        """Sets the membership_start_date of this SaleItensViewModel.


        :param membership_start_date: The membership_start_date of this SaleItensViewModel.  # noqa: E501
        :type: datetime
        """

        self._membership_start_date = membership_start_date

    @property
    def discount(self):
        """Gets the discount of this SaleItensViewModel.  # noqa: E501


        :return: The discount of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._discount

    @discount.setter
    def discount(self, discount):
        """Sets the discount of this SaleItensViewModel.


        :param discount: The discount of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._discount = discount

    @property
    def corporate_discount(self):
        """Gets the corporate_discount of this SaleItensViewModel.  # noqa: E501


        :return: The corporate_discount of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._corporate_discount

    @corporate_discount.setter
    def corporate_discount(self, corporate_discount):
        """Sets the corporate_discount of this SaleItensViewModel.


        :param corporate_discount: The corporate_discount of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._corporate_discount = corporate_discount

    @property
    def tax(self):
        """Gets the tax of this SaleItensViewModel.  # noqa: E501


        :return: The tax of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._tax

    @tax.setter
    def tax(self, tax):
        """Sets the tax of this SaleItensViewModel.


        :param tax: The tax of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._tax = tax

    @property
    def voucher(self):
        """Gets the voucher of this SaleItensViewModel.  # noqa: E501


        :return: The voucher of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._voucher

    @voucher.setter
    def voucher(self, voucher):
        """Sets the voucher of this SaleItensViewModel.


        :param voucher: The voucher of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._voucher = voucher

    @property
    def accounting_code(self):
        """Gets the accounting_code of this SaleItensViewModel.  # noqa: E501


        :return: The accounting_code of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._accounting_code

    @accounting_code.setter
    def accounting_code(self, accounting_code):
        """Sets the accounting_code of this SaleItensViewModel.


        :param accounting_code: The accounting_code of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._accounting_code = accounting_code

    @property
    def municipal_service_code(self):
        """Gets the municipal_service_code of this SaleItensViewModel.  # noqa: E501


        :return: The municipal_service_code of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._municipal_service_code

    @municipal_service_code.setter
    def municipal_service_code(self, municipal_service_code):
        """Sets the municipal_service_code of this SaleItensViewModel.


        :param municipal_service_code: The municipal_service_code of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._municipal_service_code = municipal_service_code

    @property
    def fl_receipt_only(self):
        """Gets the fl_receipt_only of this SaleItensViewModel.  # noqa: E501


        :return: The fl_receipt_only of this SaleItensViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._fl_receipt_only

    @fl_receipt_only.setter
    def fl_receipt_only(self, fl_receipt_only):
        """Sets the fl_receipt_only of this SaleItensViewModel.


        :param fl_receipt_only: The fl_receipt_only of this SaleItensViewModel.  # noqa: E501
        :type: bool
        """

        self._fl_receipt_only = fl_receipt_only

    @property
    def id_sale_item_migration(self):
        """Gets the id_sale_item_migration of this SaleItensViewModel.  # noqa: E501


        :return: The id_sale_item_migration of this SaleItensViewModel.  # noqa: E501
        :rtype: str
        """
        return self._id_sale_item_migration

    @id_sale_item_migration.setter
    def id_sale_item_migration(self, id_sale_item_migration):
        """Sets the id_sale_item_migration of this SaleItensViewModel.


        :param id_sale_item_migration: The id_sale_item_migration of this SaleItensViewModel.  # noqa: E501
        :type: str
        """

        self._id_sale_item_migration = id_sale_item_migration

    @property
    def fl_swimming(self):
        """Gets the fl_swimming of this SaleItensViewModel.  # noqa: E501


        :return: The fl_swimming of this SaleItensViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._fl_swimming

    @fl_swimming.setter
    def fl_swimming(self, fl_swimming):
        """Sets the fl_swimming of this SaleItensViewModel.


        :param fl_swimming: The fl_swimming of this SaleItensViewModel.  # noqa: E501
        :type: bool
        """

        self._fl_swimming = fl_swimming

    @property
    def fl_allow_locker(self):
        """Gets the fl_allow_locker of this SaleItensViewModel.  # noqa: E501


        :return: The fl_allow_locker of this SaleItensViewModel.  # noqa: E501
        :rtype: bool
        """
        return self._fl_allow_locker

    @fl_allow_locker.setter
    def fl_allow_locker(self, fl_allow_locker):
        """Sets the fl_allow_locker of this SaleItensViewModel.


        :param fl_allow_locker: The fl_allow_locker of this SaleItensViewModel.  # noqa: E501
        :type: bool
        """

        self._fl_allow_locker = fl_allow_locker

    @property
    def id_member_membership(self):
        """Gets the id_member_membership of this SaleItensViewModel.  # noqa: E501


        :return: The id_member_membership of this SaleItensViewModel.  # noqa: E501
        :rtype: int
        """
        return self._id_member_membership

    @id_member_membership.setter
    def id_member_membership(self, id_member_membership):
        """Sets the id_member_membership of this SaleItensViewModel.


        :param id_member_membership: The id_member_membership of this SaleItensViewModel.  # noqa: E501
        :type: int
        """

        self._id_member_membership = id_member_membership

    @property
    def value_next_month(self):
        """Gets the value_next_month of this SaleItensViewModel.  # noqa: E501


        :return: The value_next_month of this SaleItensViewModel.  # noqa: E501
        :rtype: float
        """
        return self._value_next_month

    @value_next_month.setter
    def value_next_month(self, value_next_month):
        """Sets the value_next_month of this SaleItensViewModel.


        :param value_next_month: The value_next_month of this SaleItensViewModel.  # noqa: E501
        :type: float
        """

        self._value_next_month = value_next_month

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(SaleItensViewModel, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SaleItensViewModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other