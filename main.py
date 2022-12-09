import sys
from enum import Enum
from termcolor import colored

users = []  # database


# <-- models start
class AccountType(Enum):
    KZT = 'KZT'
    USD = 'USD'
    RUB = 'RUB'
    EUR = 'EUR'


class Account:
    amount: float
    account_type: AccountType

    def __init__(self, account_type: AccountType):
        self.amount = 0.00
        self.account_type = account_type

    @property
    def current_account_type(self):
        return {self.account_type.value}

    @current_account_type.setter
    def current_account_type(self, another_type: AccountType):
        self.account_type = another_type


class BankAccount:
    account: Account

    def __init__(self, name: str, surname: str, account: Account):
        self.name = name
        self.surname = surname
        self.account = account

    def __str__(self):
        return f'У вас на счету {self.account.amount} {self.account.account_type.value}'

    def __del__(self):
        return f'Аккаунт {self.name} {self.surname} был удален'

    def add_to_bank_account(self, value):
        self.account.amount += value

    def substract_from_bank_account(self, value):
        self.account.amount -= value

    @staticmethod
    def moneyConversion(conversion_amount, currency_from, currency_to) -> float:
        match currency_from, currency_to:
            # KZT operations
            case 'KZT', 'USD':
                return round(conversion_amount / 470, 2)
            case 'KZT', 'RUB':
                return round(conversion_amount / 7.5, 2)
            case 'KZT', 'EUR':
                return round(conversion_amount / 490, 2)
            # USD Operations
            case 'USD', 'KZT':
                return round(conversion_amount * 470, 2)
            case 'USD', 'EUR':
                return round(conversion_amount / 1.04, 2)
            case 'USD', 'RUB':
                return round(conversion_amount * 62.8, 2)
            # EUR Operations
            case 'EUR', 'KZT':
                return round(conversion_amount * 490, 2)
            case 'EUR', 'USD':
                return round(conversion_amount * 1.04, 2)
            case 'EUR', 'RUB':
                return round(conversion_amount * 65.6, 2)
            # RUB Operations
            case 'RUB', 'KZT':
                return round(conversion_amount * 7.5, 2)
            case 'RUB', 'USD':
                return round(conversion_amount / 62.8, 2)
            case 'RUB', 'EUR':
                return round(conversion_amount / 65.6, 2)

    # Перевод средств между пользователями
    def tranfer(self, transfer_amount: float, person: list[object]):
        self.account.amount -= transfer_amount
        if self.account.account_type.value != person.account.account_type.value:
            transfer_amount = self.moneyConversion(
                transfer_amount,
                self.account.account_type.value,
                person.account.account_type.value
            )
        person.account.amount += transfer_amount


# models end -->

# <-- repo start
def create_user(name: str, surname: str, account: Account) -> None:
    user = BankAccount(name, surname, account)
    users.append(user)


def get_user(name: str, surname: str) -> BankAccount:
    try:
        user = next(u for u in users if name == u.name and surname == u.surname)
    except:
        print(colored('Пользователь не найден', 'red'))
        return
    return user


def currency_checker(currency: str) -> AccountType:
    match currency:
        case AccountType.USD.value:
            return AccountType.USD
        case AccountType.RUB.value:
            return AccountType.RUB
        case AccountType.KZT.value:
            return AccountType.KZT
        case AccountType.EUR.value:
            return AccountType.EUR
        case _:
            print(colored('Неккоректная валюта', 'red'))
            return


# repo end -->

# <-- terminal menu start
while True:
    command = input('Введите команду:\nСоздать|Выбрать|Выйти\n').capitalize()
    match command:
        case 'Создать':
            name = input('Введите Имя:\n')
            surname = input('Введите фамилию:\n')
            currency = input('Введите валюту в которой будете хранить Ваши средства\n(USD,KZT,EUR,RUB)\n').upper()
            result = currency_checker(currency)
            account = Account(account_type=result)
            create_user(name, surname, account)
        case 'Выбрать':
            name = input('Введите Имя:\n')
            surname = input('Введите фамилию:\n')
            user = get_user(name, surname)
            if user:
                print(f'Добро пожаловать {user.name} {user.surname}')
                while True:
                    bank_command = input('Вы можете воспользоваться следующим списком команд:'
                                         '\nОстаток счета|Пополнить|Вывести|Обмен валюты|Перевести|Удалить|Выйти\n').capitalize()
                    match bank_command:
                        case 'Остаток счета':
                            print(user)
                        case 'Пополнить':
                            amount = int(input('Введите сумму пополнения:\n'))
                            user.add_to_bank_account(amount)
                            print('Счет успешно пополнен')
                        case 'Вывести':
                            amount = int(input('Введите сумму для вывода средств:\n'))
                            if user.account.amount < amount:
                                print(colored('У Вас недостаточно средств', 'red'))
                                continue
                            user.substract_from_bank_account(amount)
                            print('Вывод средств успешно выполнен')
                        case 'Обмен валюты':
                            conversion_amount = int(input('Введите сумму, которую желаете обменять:\n'))
                            currency_from = input('Укажите нынешнюю валюту:\n').upper()
                            result_from = currency_checker(currency_from)
                            currency_to = input('Укажите валюту,на которую желаете обменять:\n').upper()
                            result_to = currency_checker(currency_to)
                            exchanged_amount = user.moneyConversion(conversion_amount, result_from.value,
                                                                    result_to.value)
                            print(f'{exchanged_amount} {result_to.value}')
                        case 'Перевести':
                            if len(users) < 2:
                                print(colored(
                                    'В базе данных только 1 пользователь, '
                                    'перевод невозможно осуществить, создайте еще одного пользователя',
                                    'red'))
                                continue

                            transfer_amount = int(input('Введите сумму перевода:\n'))
                            if user.account.amount < transfer_amount:
                                print(colored('У Вас недостаточно средств', 'red'))
                                continue
                            recipient_name = input('Введите имя получателя\n')
                            recipient_surname = input('Введите фамилию получателя\n')
                            person = get_user(recipient_name, recipient_surname)
                            user.tranfer(transfer_amount, person)
                            print(f'Сумма в размере {transfer_amount} {user.account.account_type.value}'
                                  f' была переведена пользователю {recipient_name} {recipient_surname}')
                        case 'Удалить':
                            answer = input('Вы уверены,что хотите удалить свой аккаунт?\n').capitalize()
                            if answer == 'Да':
                                del user
                                print('Аккаунт успешно удален')
                                break
                            elif answer == 'Нет':
                                continue
                        case 'Выйти':
                            break
                        case _:
                            print(colored('Неккоректная команда', 'red'))

        case 'Выйти':
            sys.exit(0)
        case _:
            print(colored('Неккоректная команда', 'red'))
# terminal menu end -->
