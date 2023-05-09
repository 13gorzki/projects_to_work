import os
import fnmatch

import pandas as pd

from modules.log_report import write_log


class Nike:
    def tabor_nike(self, from_file):
        df_nike = pd.read_csv(from_file, sep=",", dtype="string")

        column_cash = ["Cena netto", "Cena hurtowa", "Sugerowana cena detaliczna"]
        gender = {
            "BOYS": "KIDS",
            "GIRLS": "KIDS",
            "MENS": "MEN",
            "NOT APPLICABLE": "",
            "UNISEX": "UNISEX",
            "WOMENS": "WOMEN",
        }
        category_group = {
            "Obuwie sportowe": "OBUWIE",
            "Odzież": "TEKSTYLIA",
            "Sprzęt": "AKCESORIA",
        }
        wrong_char = {
            "Ą": "A",
            "Ć": "C",
            "Ę": "E",
            "Ł": "L",
            "Ń": "N",
            "Ó": "O",
            "Ś": "S",
            "Ź": "Z",
            "Ż": "Z",
            "'": "",
            '"': "",
            "®": "",
            "’": "",
            "\xa0": "",
            "  ": " ",
        }

        df_nike["Potwierdzone"] = df_nike["Potwierdzone"].astype("int")

        for column in column_cash:
            df_nike[column] = df_nike[column].str.replace(" zł", "")
            df_nike[column] = df_nike[column].str.replace(",", ".")
            df_nike[column] = df_nike[column].str.replace("\xa0", "")
            df_nike[column] = df_nike[column].astype("float")

        df_tabor = pd.DataFrame(
            columns=[
                "Order_ConfirmedAmount",
                "Order_ConfirmedQuantity",
                "OrderCompany_SoldTo",
                "Product_StyleDesc",
                "Product_MaterialNumber",
                "Order_CCD_SeasonYear",
                "Order_CRD",
                "OrderH_OrderNumber",
                "OrderShop_ShipTo",
                "Product_Price_Retail",
                "Size_SizeCode",
                "Product_Price_Wholesale",
                "EAN",
                "Kupiec",
                "Marka",
                "Rabat",
                "Opis zamowienia",
                "Zamowienie_pod_koncept",
                "Grupa",
                "Przeznaczenie",
                "Gender",
                "CenaZakJedn",
                "VATzak",
                "VATspr",
                "PaymTerm",
                "ILN",
            ]
        )

        df_tabor["Order_ConfirmedAmount"] = (
            df_nike["Potwierdzone"] * df_nike["Cena netto"]
        ).round(2)
        df_tabor["Order_ConfirmedQuantity"] = df_nike["Potwierdzone"]
        df_tabor["OrderCompany_SoldTo"] = df_nike["Numer zamawiającego"]
        df_tabor["Product_StyleDesc"] = df_nike["Nazwa stylu"] + df_nike["Opis koloru"]
        df_tabor["Product_StyleDesc"] = df_tabor["Product_StyleDesc"].str.upper()
        df_tabor["Product_MaterialNumber"] = df_nike["Numer koloru modelu"]
        df_tabor["Order_CCD_SeasonYear"] = (
            pd.to_datetime(df_nike["Data CRD pozycji"], format="%d.%m.%y").dt.strftime(
                "%y"
            )
            + "Q"
            + pd.to_datetime(
                df_nike["Data CRD pozycji"], format="%d.%m.%y"
            ).dt.quarter.astype("string")
        )
        df_tabor["Order_CRD"] = pd.to_datetime(
            df_nike["Data CRD pozycji"], format="%d.%m.%y"
        )
        df_tabor["OrderH_OrderNumber"] = df_nike["Zamówienie nr"].astype("string")
        df_tabor["OrderShop_ShipTo"] = df_nike["Numer odbiorcy"].astype("string")
        df_tabor["Product_Price_Retail"] = df_nike["Sugerowana cena detaliczna"]
        df_tabor["Size_SizeCode"] = df_nike["Rozmiar"]
        df_tabor["Product_Price_Wholesale"] = df_nike["Cena hurtowa"]
        df_tabor["EAN"] = df_nike["Kod paskowy"]
        # df_tabor['Kupiec'] = df_nike['''']
        df_tabor["Marka"] = "NIKE"
        df_tabor["Rabat"] = (
            (df_nike["Cena hurtowa"] - df_nike["Cena netto"]) / df_nike["Cena hurtowa"]
        ).round(2)
        df_tabor["Opis zamowienia"] = df_nike["PO nr"]
        # df_tabor['Zamowienie_pod_koncept'] = df_nike['']
        df_tabor["Grupa"] = df_nike["Dział produktu"]
        # df_tabor['Przeznaczenie'] = df_nike['']
        df_tabor["Gender"] = df_nike["Płeć/wiek"]
        df_tabor["CenaZakJedn"] = df_nike["Cena netto"]
        df_tabor["VATzak"] = 0
        df_tabor["VATspr"] = 23
        df_tabor["PaymTerm"] = df_nike["Termin zapłaty za pozycję"].str.replace(
            "Net ", ""
        )  # .astype('int')
        df_tabor["ILN"] = "496739"

        df_tabor = df_tabor.replace({"Gender": gender})
        df_tabor = df_tabor.replace({"Grupa": category_group})

        for col in df_tabor.columns:
            if df_tabor[col].dtypes == "string":
                for char in wrong_char:
                    df_tabor[col] = df_tabor[col].str.replace(char, wrong_char[char])

        return df_tabor

    # def kartoteka(self, from_file):
    #     df_nike = pd.read_csv(from_file, sep=',', dtype='string')
    #
    #     column_cash = ['Cena netto', 'Cena hurtowa', 'Sugerowana cena detaliczna']
    #     gender = {'BOYS': 'KIDS', 'GIRLS': 'KIDS', 'MENS': 'MEN', 'NOT APPLICABLE': '', 'UNISEX': 'UNISEX',
    #               'WOMENS': 'WOMEN'}
    #     category_group = {'Obuwie sportowe': 'OBUWIE', 'Odzież': 'TEKSTYLIA', 'Sprzęt': 'AKCESORIA'}
    #     wrong_char = {'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
    #                   '\'': '', '"': '', '®': '', '’': '', u'\xa0': '', '  ': ' '}
    #
    #     df_nike['Potwierdzone'] = df_nike['Potwierdzone'].astype('int')
    #
    #     for column in column_cash:
    #         df_nike[column] = df_nike[column].str.replace(' zł', '')
    #         df_nike[column] = df_nike[column].str.replace(',', '.')
    #         df_nike[column] = df_nike[column].str.replace(u'\xa0', '')
    #         df_nike[column] = df_nike[column].astype('float')
