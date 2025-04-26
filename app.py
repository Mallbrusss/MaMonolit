import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os


# URL вашего API
API_URL = "http://localhost:8080/api/v1/sig/getSignals"

# Список доступных тикеров
TICKERS = [
            {"figi": "BBG004730JJ5", "ticker": "MOEX", "instrumentId": "5e1c2634-afc4-4e50-ad6d-f78fc14a539a"},
            {"figi":"TCS007940839","ticker":"KZIZP","instrumentId":"9b5f01f6-b836-45e4-af1b-e23cbab34507"},
            {"figi":"TCS10A0JR514","ticker":"LIFE","instrumentId":"40ca6061-9acc-40ec-9571-4c41b10730d9"},
            {"figi":"TCS00A108ZR8","ticker":"DATA","instrumentId":"0b9afb23-280f-4fda-a7ad-816994959c6b"},
            {"figi":"BBG000FWGSZ5","ticker":"IRKT","instrumentId":"cfb50a23-2465-497e-bc7e-e4f0e042cf3d"},
            {"figi":"BBG004S68CV8","ticker":"VSMO","instrumentId":"e9139ddd-bf3c-4d03-a94f-ffdf7234c6be"},
            {"figi":"BBG000Q7ZZY2","ticker":"UNAC","instrumentId":"43666aea-a4df-46e1-a815-e5eccbc1fb3f"},
            {"figi":"TCS00A106YF0","ticker":"VKCO","instrumentId":"b71bd174-c72c-41b0-a66f-5f9073e0d1f5"},
            {"figi":"TCS0418T1088","ticker":"CIAN@US","instrumentId":"02afac94-15ea-4586-b1da-8704b65daf2f"},
            {"figi":"BBG000RJL816","ticker":"TTLK","instrumentId":"76721c1c-52a9-4b45-987e-d075f651f1b1"},
            {"figi":"BBG004RVFCY3","ticker":"MGNT","instrumentId":"ca845f68-6c43-44bc-b584-330d2a1e5eb7"},
            {"figi":"TCS00A0ZZAC4","ticker":"SVCB","instrumentId":"1fbecbbc-ef32-448c-b4fe-b0037795ba01"},
            {"figi":"TCS009124010","ticker":"KZIZ","instrumentId":"0f3165ef-3b53-4bc0-a4c8-19d0016b0b6d"},
            {"figi":"BBG001M2SC01","ticker":"ETLN","instrumentId":"a9b8460b-0272-49a6-b803-4c02d3e9c5d9"},
            {"figi":"BBG0029SG1C1","ticker":"KZOSP","instrumentId":"3879e073-f27a-4e2f-9a97-97475b25194d"},
            {"figi":"TCS00A105EX7","ticker":"WUSH","instrumentId":"b993e814-9986-4434-ae88-b086066714a0"},
            {"figi":"TCS00A107JE2","ticker":"GEMC","instrumentId":"fbc2eb4e-997e-4654-a1b1-4055e238bd00"},
            {"figi":"TCS00A0JPP37","ticker":"UGLD","instrumentId":"48bd9002-43be-4528-abf4-dc8135ad4550"},
            {"figi":"BBG004S689R0","ticker":"PHOR","instrumentId":"9978b56f-782a-4a80-a4b1-a48cbecfd194"},
            {"figi":"TCS00A106XF2","ticker":"HNFG","instrumentId":"2fa1d15e-236c-4e4e-8155-f740badfece6"},
            {"figi":"TCS2207L1061","ticker":"HHRU","instrumentId":"cf9ed7ef-784d-4c2c-aabe-362891fcd80c"},
            {"figi":"BBG000SK7JS5","ticker":"LNZL","instrumentId":"4563f7a1-8245-4caf-aba5-ac49827ba775"},
            {"figi":"BBG002458LF8","ticker":"SELG","instrumentId":"0d28c01b-f841-4e89-9c92-0ee23d12883a"},
            {"figi":"BBG004S68829","ticker":"TATNP","instrumentId":"efdb54d3-2f92-44da-b7a3-8849e96039f6"},
            {"figi":"TCS009086904","ticker":"SLAV","instrumentId":"2c69924a-fcf4-4d3c-8c02-02cd665f554d"},
            {"figi":"TCS00A0JNXF9","ticker":"PRFN","instrumentId":"16bb8ed3-2cb1-4d89-8f04-afe0b34e21d0"},
            {"figi":"BBG004S68507","ticker":"MAGN","instrumentId":"7132b1c9-ee26-4464-b5b5-1046264b61d9"},
            {"figi":"BBG004730ZJ9","ticker":"VTBR","instrumentId":"8e2b0325-0292-4654-8a18-4f63ed3b0e09"},
            {"figi":"TCS00A105NV2","ticker":"CARM","instrumentId":"330a4507-03f9-4f8d-8303-492ba09cccba"},
            {"figi":"BBG008F2T3T2","ticker":"RUAL","instrumentId":"f866872b-8f68-4b6e-930f-749fe9aa79c0"},
            {"figi":"BBG00BGKYH17","ticker":"NKHP","instrumentId":"d0b3723c-35f8-497c-97f7-345bbcfbf1e1"},
            {"figi":"TCS00A0F61T7","ticker":"TGKJ","instrumentId":"0102d253-5095-499c-934e-5a5fd6fce00d"},
            {"figi":"BBG004S686N0","ticker":"BANEP","instrumentId":"a5776620-1e2f-47ea-bbd6-06d8e4a236d8"},
            {"figi":"BBG00172J7S9","ticker":"OKEY","instrumentId":"2a3ac153-f5fb-4f6d-af66-38a8d2b2eacb"},
            {"figi":"BBG004S68B31","ticker":"ALRS","instrumentId":"30817fea-20e6-4fee-ab1f-d20fc1a1bb72"},
            {"figi":"BBG000VG1034","ticker":"MRKP","instrumentId":"9a41ec6e-edf0-4863-9ec0-fb3a5c6811e2"},
            {"figi":"BBG000R04X57","ticker":"FLOT","instrumentId":"21423d2d-9009-4d37-9325-883b368d13ae"},
            {"figi":"TCS00A107ER5","ticker":"DIAS","instrumentId":"3f692296-eee8-4854-a905-019d6377961f"},
            {"figi":"BBG004RVFFC0","ticker":"TATN","instrumentId":"88468f6c-c67a-4fb4-a006-53eed803883c"},
            {"figi":"TCS60A0JQ9P9","ticker":"SPBE","instrumentId":"15dc2120-29d2-48b8-87c0-da1d95255f68"},
            {"figi":"TCS10A0JNAB6","ticker":"ABIO","instrumentId":"cbdf1d32-5758-490e-a2b1-780eaa79bdf7"},
            {"figi":"BBG000V07CB8","ticker":"DVEC","instrumentId":"18fb3421-7637-48f1-b5b5-20a454e1af5b"},
            {"figi":"TCS0760G1031","ticker":"ETLN@GS","instrumentId":"d0728bc1-51b4-47bc-9a7f-2a306892ffa4"},
            {"figi":"BBG004S682Z6","ticker":"RTKM","instrumentId":"02eda274-10c4-4815-8e02-a8ee7eaf485b"},
            {"figi":"TCS30A108JF7","ticker":"PRMD","instrumentId":"2ce7103b-d526-4c71-87be-0bd3f49a8b51"},
            {"figi":"TCS00A107RM8","ticker":"ZAYM","instrumentId":"1a7766fb-3aa9-4b20-8817-b9b7607c0e7b"},
            {"figi":"BBG004S681W1","ticker":"MTSS","instrumentId":"cd8063ad-73ad-4b31-bd0d-93138d9e99a2"},
            {"figi":"TCS1949E2046","ticker":"GLTR@GS","instrumentId":"38be8280-96ef-45e9-b0ed-da76bc77fe7c"},
            {"figi":"TCS00A109B25","ticker":"OZPH","instrumentId":"aeb8e3c7-b547-4073-b9cd-575590e1576d"},
            {"figi":"BBG000RG4ZQ4","ticker":"TGKN","instrumentId":"41133bf9-9b9d-4d28-8864-9160b57871d1"},
            {"figi":"BBG00475KHX6","ticker":"TRNFP","instrumentId":"653d47e9-dbd4-407a-a1c3-47f897df4694"},
            {"figi":"BBG00475JZZ6","ticker":"FEES","instrumentId":"88e130e8-5b68-4b05-b9ae-baf32f5a3f21"},
            {"figi":"TCS00A0HG6Z8","ticker":"OBNE","instrumentId":"ffac99ad-bafa-430e-9750-e77a43176ede"},
            {"figi":"BBG000MZL0Y6","ticker":"PMSB","instrumentId":"4d8209f9-3b75-437d-ad5f-2906d56f27e9"},
            {"figi":"TCS10A0JR6A6","ticker":"RBCM","instrumentId":"45fb6af4-9076-4268-b038-ab7f37d15ab2"},
            {"figi":"BBG000QFB4J6","ticker":"ZILLP","instrumentId":"f4da07c8-dfc5-44f8-989d-c45d85027aad"},
            {"figi":"BBG004S687G6","ticker":"MSRS","instrumentId":"019029c2-6634-4536-a980-389575e09b74"},
            {"figi":"TCS90A0JQUZ6","ticker":"RAGR","instrumentId":"9b9a584e-448f-40da-9ba8-353b44ad697a"},
            {"figi":"BBG004S68473","ticker":"IRAO","instrumentId":"2dfbc1fd-b92a-436e-b011-928c79e805f2"},
            {"figi":"BBG002BCQK67","ticker":"NSVZ","instrumentId":"88c3b1dd-cf86-48b6-b479-464ce1149472"},
            {"figi":"BBG000RTHVK7","ticker":"GCHE","instrumentId":"231e5e27-9956-47e7-ad50-6e802e4a92ed"},
            {"figi":"TCS90A0JVBT9","ticker":"UWGN","instrumentId":"17017bf0-ed5c-47be-8fae-c0cedbfabe32"},
            {"figi":"BBG004S681M2","ticker":"SNGSP","instrumentId":"a797f14a-8513-4b84-b15e-a3b98dc4cc00"},
            {"figi":"TCS20A0J2QG8","ticker":"BLNG","instrumentId":"f93377cf-2944-47bb-a90f-25359d2f133c"},
            {"figi":"TCS03A108X38","ticker":"X5","instrumentId":"0964acd0-e2cb-4810-a177-ef4ad8856ff0"},
            {"figi":"BBG00475KKY8","ticker":"NVTK","instrumentId":"0da66728-6c30-44c4-9264-df8fac2467ee"},
            {"figi":"BBG002YFXL29","ticker":"UNKL","instrumentId":"69e56041-ddab-4151-9832-e0a1e9f83a42"},
            {"figi":"BBG000GQSRR5","ticker":"NKNC","instrumentId":"7fad3575-99ca-4b36-807c-9c7c37e64b29"},
            {"figi":"BBG000W325F7","ticker":"AQUA","instrumentId":"b83ab195-dcd2-4d44-b9bf-27fa294f19a0"},
            {"figi":"BBG000BX7DH0","ticker":"VRSB","instrumentId":"3c899002-e8f5-42fd-b617-4bc2f31e6767"},
            {"figi":"TCS00A0JRH43","ticker":"MBNK","instrumentId":"459a1a0a-0253-465a-bd4e-afaaf5e670b0"},
            {"figi":"BBG004Z2RGW8","ticker":"ROLO","instrumentId":"eb05ebd4-a216-434b-bddd-69531f120ec9"},
            {"figi":"BBG000RK52V1","ticker":"OGKB","instrumentId":"3d8f2777-4a11-4713-af60-8038d11e66fa"},
            {"figi":"TCS009084453","ticker":"NOMP","instrumentId":"b24fa6a8-b700-4afb-8e24-2c7ed5e4888e"},
            {"figi":"BBG000QCW561","ticker":"VEON","instrumentId":"e58eec43-da4f-45bb-98e2-1bdb8d1bc6ff"},
            {"figi":"BBG002B9T6Y1","ticker":"KAZTP","instrumentId":"3240b205-4718-47d2-8650-8bdc89533fd8"},
            {"figi":"BBG0047315D0","ticker":"SNGS","instrumentId":"1ffe1bff-d7b7-4b04-b482-34dc9cc0a4ba"},
            {"figi":"BBG009GSYN76","ticker":"CBOM","instrumentId":"ebfda284-4291-4337-9dfb-f55610d0a907"},
            {"figi":"BBG000RJWGC4","ticker":"AMEZ","instrumentId":"08da2447-0dc4-433d-a2f3-627382208695"},
            {"figi":"BBG000Q7GJ60","ticker":"TGKBP","instrumentId":"45609688-b63e-42dd-88a0-9d30c423c5e5"},
            {"figi":"BBG002W2FT69","ticker":"ABRD","instrumentId":"926fdfbf-4b07-47c9-8928-f49858ca33f2"},
            {"figi":"BBG004S68BH6","ticker":"PIKK","instrumentId":"03d5e771-fc10-438e-8892-85a40733612d"},
            {"figi":"BBG004731354","ticker":"ROSN","instrumentId":"fd417230-19cf-4e7b-9623-f7c9ca18ec6b"},
            {"figi":"TCS00A1002V2","ticker":"EUTR","instrumentId":"02b2ea14-3c4b-47e8-9548-45a8dbcc8f8a"},
            {"figi":"BBG004TC84Z8","ticker":"TRMK","instrumentId":"278d9ccc-4dde-484e-bf79-49ce8f733470"},
            {"figi":"TCS00A0ZZBC2","ticker":"SOFL","instrumentId":"ab1f751e-15b2-4c74-802c-1b3e8638c394"},
            {"figi":"BBG000VKG4R5","ticker":"MRKU","instrumentId":"1b64e38a-49ad-4f4d-a4d3-b34184899352"},
            {"figi":"BBG002B2J5X0","ticker":"KRKNP","instrumentId":"6891e539-6070-4ba6-99c0-7eb1df9c816e"},
            {"figi":"BBG00475K6C3","ticker":"CHMF","instrumentId":"fa6aae10-b8d5-48c8-bbfd-d320d925d096"},
            {"figi":"BBG000RMWQD4","ticker":"ENPG","instrumentId":"e2bd2eba-75de-4127-b39c-2f2dbe3866c3"},
            {"figi":"BBG000GQSVC2","ticker":"NKNCP","instrumentId":"bc21fb4f-8838-4355-8697-fb0d8fc809c8"},
            {"figi":"TCS00A0HG602","ticker":"OBNEP","instrumentId":"69f5da81-80c7-4c12-85dc-3bb7524c4a35"},
            {"figi":"TCS80A107UL4","ticker":"T","instrumentId":"87db07bc-0e02-4e29-90bb-05e8ef791d7b"},
            {"figi":"TCS009102396","ticker":"UFOSP","instrumentId":"e0e1ee47-d3e6-43d9-9755-44dcc18ab271"},
            {"figi":"BBG000PKWCQ7","ticker":"MRKV","instrumentId":"8ec4edb6-b779-4e3c-9146-b11210174d51"},
            {"figi":"TCS4387E2054","ticker":"FIVE@GS","instrumentId":"aa183ebe-3dae-4f4b-b7a2-c03539375417"},
            {"figi":"BBG004S68C39","ticker":"LSRG","instrumentId":"b2db7bb1-6f04-4c3c-b910-fb7fd8aab52d"},
            {"figi":"BBG000BBV4M5","ticker":"CNTL","instrumentId":"c05fd0a1-0c8e-4bc3-bf9e-43e364d278ef"},
            {"figi":"TCS10A108K09","ticker":"VSEH","instrumentId":"538a1b13-df23-4449-8302-e8adbc25daf4"},
            {"figi":"BBG004S68JR8","ticker":"SVAV","instrumentId":"c3746fd5-ac02-419a-8893-827775cfb2c8"},
            {"figi":"BBG004S685M3","ticker":"RTKMP","instrumentId":"e1b089f3-9bf1-44c3-897f-25e9f591bebc"},
            {"figi":"BBG000LNHHJ9","ticker":"KMAZ","instrumentId":"f8f1de0d-5a5f-47e9-8ecb-00bec8f8351f"},
            {"figi":"BBG0029SFXB3","ticker":"KZOS","instrumentId":"a6121478-943f-4eae-bc2a-bab5c771dd4a"},
            {"figi":"BBG000PZ0833","ticker":"MGTSP","instrumentId":"3112d684-216c-4409-ab73-4316e8582f81"},
            {"figi":"BBG000F6YPH8","ticker":"ELFV","instrumentId":"93e0d4c6-45c9-4399-9e0b-dc2f2ff101c7"},
            {"figi":"TCS00A107KX0","ticker":"KLVZ","instrumentId":"e3f629fd-367b-4dbd-922c-4a4c130c70ab"},
            {"figi":"BBG00R4Z2NT4","ticker":"VEON-RX","instrumentId":"f1374f83-7934-41f7-a210-097ed5beecd5"},
            {"figi":"TCS002614686","ticker":"NTZL","instrumentId":"c09c1942-68a1-40c3-97e3-3a91ac08efe5"},
            {"figi":"TCS20A107662","ticker":"HEAD","instrumentId":"3fe80143-1313-42eb-9884-5d68b39e265e"},
            {"figi":"TCS609805522","ticker":"YNDX@US","instrumentId":"6fdc957d-0062-48fc-9b6c-dcf64f3c966a"},
            {"figi":"TCS00A107T19","ticker":"YDEX","instrumentId":"7de75794-a27f-4d81-a39b-492345813822"},
            {"figi":"BBG00F6NKQX3","ticker":"SMLT","instrumentId":"4d813ab1-8bc9-4670-89ea-12bfbab6017d"},
            {"figi":"BBG004S68758","ticker":"BANE","instrumentId":"0a55e045-e9a6-42d2-ac55-29674634af2f"},
            {"figi":"BBG004S683W7","ticker":"AFLT","instrumentId":"1c69e020-f3b1-455c-affa-45f8b8049234"},
            {"figi":"BBG001BBGNS2","ticker":"ORUP","instrumentId":"85d3979a-8e8c-4652-8b61-2c020613ee70"},
            {"figi":"BBG004730N88","ticker":"SBER","instrumentId":"e6123145-9665-43e0-8413-cd61b8aa9b13"},
            {"figi":"TCS50A102093","ticker":"ELMT","instrumentId":"f1b89b92-51e2-4db5-89df-17c228aa41fd"},
            {"figi":"TCS00A105BN4","ticker":"GECO","instrumentId":"c74fc209-54e2-4ba6-a7a9-9e0d24299184"},
            {"figi":"BBG004S68CP5","ticker":"MVID","instrumentId":"cf1c6158-a303-43ac-89eb-9b1db8f96043"},
            {"figi":"BBG000MZL2S9","ticker":"PMSBP","instrumentId":"80a39145-b2f7-46f5-9ef0-1478baafb0a6"},
            {"figi":"BBG004S68DD6","ticker":"MSTT","instrumentId":"3058acbe-11f6-4bcc-9a70-238e70c2c588"},
            {"figi":"BBG004S68598","ticker":"MTLR","instrumentId":"eb4ba863-e85f-4f80-8c29-f2627938ee58"},
            {"figi":"TCS00A108GD8","ticker":"IVAT","instrumentId":"1936e51c-d914-4171-ac66-6390a605cb5b"},
            {"figi":"BBG004S688G4","ticker":"AKRN","instrumentId":"cd3affd4-3b50-43fd-b008-518f54108d59"},
            {"figi":"TCS00Y3XYV94","ticker":"MDMG","instrumentId":"0d53d29a-3794-41c6-ba72-556d46bacb46"},
            {"figi":"BBG004730RP0","ticker":"GAZP","instrumentId":"962e2a95-02a9-4171-abd7-aa198dbe643a"},
            {"figi":"BBG0047315Y7","ticker":"SBERP","instrumentId":"c190ff1f-1447-4227-b543-316332699ca5"},
            {"figi":"BBG0063FKTD9","ticker":"LENT","instrumentId":"5f1e6b0a-4413-489c-b336-40b43730eaf5"},
            {"figi":"BBG000QJW156","ticker":"BSPB","instrumentId":"1e19953d-01c6-4ecd-a5f4-53ae3ed44029"},
            {"figi":"RU000A106T36","ticker":"ASTR","instrumentId":"aae786d8-e8f4-4428-91bb-cffa39ad01e4"},
            {"figi":"BBG000LWNRP3","ticker":"RKKE","instrumentId":"303100b7-4c5c-4fea-8834-d0b675855527"},
            {"figi":"BBG000NLC9Z6","ticker":"LSNG","instrumentId":"02bdfa7c-ae6c-4cbd-9784-f3457dfdcedc"},
            {"figi":"BBG00QKJSX05","ticker":"RENI","instrumentId":"a57d3a52-63d5-417b-b66d-c6114587f0ea"},
            {"figi":"BBG000VH7TZ8","ticker":"MRKC","instrumentId":"e79680ec-c32b-4b14-bf6f-8ef6e143a41b"},
            {"figi":"TCS00A103X66","ticker":"POSI","instrumentId":"de08affe-4fbd-454e-9fd1-46a81b23f870"},
            {"figi":"BBG000NLB2G3","ticker":"KROT","instrumentId":"14d147b9-d977-438a-80c0-441e5589da30"},
            {"figi":"BBG002B9MYC1","ticker":"KAZT","instrumentId":"31defde8-cdc3-42bb-96bd-e2b42e825b62"},
            {"figi":"BBG004S684M6","ticker":"SIBN","instrumentId":"9ba367af-dfbd-4d9c-8730-4b1d5a47756e"},
            {"figi":"BBG002B298N6","ticker":"YAKG","instrumentId":"6e24431b-12fc-423b-b566-f2919ebd5a53"},
            {"figi":"BBG000Q7GG57","ticker":"TGKB","instrumentId":"ba9b6eb4-614c-4be8-bdba-dd86cdfece64"},
            {"figi":"BBG000DBD6F6","ticker":"KLSB","instrumentId":"8a23dd3b-04bb-41f3-a531-1bc3c08deecf"},
            {"figi":"BBG000RP8V70","ticker":"CHMK","instrumentId":"b5e26096-d013-48e4-b2a9-2f38b6090feb"},
            {"figi":"BBG00F9XX7H4","ticker":"RNFT","instrumentId":"c7485564-ed92-45fd-a724-1214aa202904"},
            {"figi":"BBG000TJ6F42","ticker":"MRKZ","instrumentId":"05dbfebd-6bc4-4645-8f21-dcf05476999d"},
            {"figi":"BBG000K3STR7","ticker":"APTK","instrumentId":"bba7a33f-48a8-4788-8469-3a9f5d668e0a"},
            {"figi":"TCS0207L1061","ticker":"HHR","instrumentId":"647532f8-a68c-479c-8dbe-fba00d392f31"},
            {"figi":"BBG005D1WCQ1","ticker":"QIWI","instrumentId":"120a928b-b2d6-45d7-a445-f6e49614ae6d"},
            {"figi":"BBG00475K2X9","ticker":"HYDR","instrumentId":"62560f05-3fd0-4d65-88f0-a27f249cc6de"},
            {"figi":"TCS03A0ZYD22","ticker":"GTRK","instrumentId":"9e69afb6-4561-4fc2-b63b-b181e3f9ecdc"},
            {"figi":"BBG004S681B4","ticker":"NLMK","instrumentId":"161eb0d0-aaac-4451-b374-f5d0eeb1b508"},
            {"figi":"BBG000TY1CD1","ticker":"BELU","instrumentId":"974077c4-d893-4058-9314-8f1b64a444b8"},
            {"figi":"BBG000SR0YS4","ticker":"LNZLP","instrumentId":"28fdec79-fcf0-40cb-b53c-586179f024e5"},
            {"figi":"BBG003LYCMB1","ticker":"SFIN","instrumentId":"55371b1f-8f7c-4c12-9d93-386fae5ec12a"},
            {"figi":"BBG000QF1Q17","ticker":"FESH","instrumentId":"11bc2246-6fde-4478-93f1-4ab90ceb4a51"},
            {"figi":"BBG004S68696","ticker":"RASP","instrumentId":"435107a9-a262-4a31-8a9b-2ee6f81c1184"},
            {"figi":"TCS009177281","ticker":"NOMPP","instrumentId":"7e58375b-01a1-4a98-850d-0f352eb078af"},
            {"figi":"BBG0100R9963","ticker":"SGZH","instrumentId":"7bedd86b-478d-4742-a28c-29d27f8dbc7d"},
            {"figi":"BBG000NLCCM3","ticker":"LSNGP","instrumentId":"698d1493-f1f7-4eff-a4d1-2e509c77bfb8"},
            {"figi":"BBG004731489","ticker":"GMKN","instrumentId":"509edd0c-129c-4ee2-934d-7f6246126da1"},
            {"figi":"BBG004S686W0","ticker":"UPRO","instrumentId":"664921c5-b552-47a6-9ced-8735a3c6ca8a"},
            {"figi":"BBG000VJMH65","ticker":"MRKS","instrumentId":"b135075c-3a05-42cf-8f55-86674d63a49d"},
            {"figi":"BBG004S687W8","ticker":"MSNG","instrumentId":"98fc1318-6990-4147-b0d1-b10999326461"},
            {"figi":"BBG004S68614","ticker":"AFKS","instrumentId":"53b67587-96eb-4b41-8e0c-d2e3c0bdd234"},
            {"figi":"BBG000R607Y3","ticker":"PLZL","instrumentId":"10620843-28ce-44e8-80c2-f26ceb1bd3e1"},
            {"figi":"BBG004731032","ticker":"LKOH","instrumentId":"02cfdf61-6298-4c0f-a9ca-9cabc82afaf3"},
            {"figi":"TCS00A107J11","ticker":"DELI","instrumentId":"df58ca03-aed0-4e1c-97fb-54a01dfb539e"},
            {"figi":"TCS00A0JVJQ8","ticker":"MGKL","instrumentId":"4dc99cf8-cb71-4dca-a74d-f70483f4d7a7"},
            {"figi":"TCS00A0ZZFS9","ticker":"LEAS","instrumentId":"ab29b599-4cb4-4b57-9c17-02b140708bf7"},
            {"figi":"TCS009046502","ticker":"UDMN","instrumentId":"42f11771-17c4-45d2-8fc5-153585b5c187"},
            {"figi":"BBG004S68BR5","ticker":"NMTP","instrumentId":"93ed8e88-2de2-4aec-a920-3384d24ecb2a"},
            {"figi":"BBG000QFH687","ticker":"TGKA","instrumentId":"d74daf58-22c3-4e44-8ada-471e404fb795"},
            {"figi":"BBG000N625H8","ticker":"FRHC","instrumentId":"3786c329-9c56-4a57-840a-a02e471f1da5"},
            {"figi":"BBG0027F0Y27","ticker":"CNTLP","instrumentId":"1fae90d9-fb73-4c28-bdc0-11f47f991a05"},
            {"figi":"BBG004S68FR6","ticker":"MTLRP","instrumentId":"c1a3c440-f51c-4a75-a400-42a2a74f5f2b"},
            {"figi":"BBG000C7P5M7","ticker":"MRKY","instrumentId":"c41a8e78-e4ee-4aa1-869a-9eff103b260a"},
]

# Интервалы свечей
INTERVALS = {
    "CANDLE_INTERVAL_UNSPECIFIED": "Не определён",
    "CANDLE_INTERVAL_1_MIN":       "от 1 минуты до 1 дня",
    "CANDLE_INTERVAL_2_MIN":       "от 2 минут до 1 дня",
    "CANDLE_INTERVAL_3_MIN":       "от 3 минут до 1 дня",
    "CANDLE_INTERVAL_5_MIN":       "от 5 минут до 1 дня",
    "CANDLE_INTERVAL_10_MIN":      "от 10 минут до 1 дня",
    "CANDLE_INTERVAL_15_MIN":      "от 15 минут до 1 дня",
    "CANDLE_INTERVAL_30_MIN":      "от 30 минут до 2 дней",
    "CANDLE_INTERVAL_HOUR":        "от 1 часа до 1 недели",
    "CANDLE_INTERVAL_2_HOUR":      "от 2 часов до 1 месяца",
    "CANDLE_INTERVAL_4_HOUR":      "от 4 часов до 1 месяца",
    "CANDLE_INTERVAL_DAY":         "от 1 дня до 1 года",
    "CANDLE_INTERVAL_WEEK":        "от 1 недели до 2 лет",
    "CANDLE_INTERVAL_MONTH":       "от 1 месяца до 10 лет"
}

# Выбор тикера
selected_ticker = st.selectbox("Выберите тикер", [ticker["ticker"] for ticker in TICKERS])

# Найти figi выбранного тикера
selected_figi = next(ticker["figi"] for ticker in TICKERS if ticker["ticker"] == selected_ticker)

selected_instrument_id = next(instrumentId["instrumentId"] for instrumentId in TICKERS if instrumentId["ticker"] == selected_ticker)

selected_interval = st.selectbox("Выберите интервал:", list(INTERVALS.keys()), format_func=lambda x: INTERVALS[x])

col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("Выберите начальную дату:")
    from_time = st.time_input("Выберите начальное время:")
with col2:
    to_date = st.date_input("Выберите конечную дату:")
    to_time = st.time_input("Выберите конечное время:")

# Преобразование даты и времени в формат ISO 8601
from_datetime = datetime.combine(from_date, from_time).isoformat() + "Z"
to_datetime = datetime.combine(to_date, to_time).isoformat() + "Z"

if from_datetime >= to_datetime:
    st.error("Начальная дата не может быть позже конечной")

# Параметры запроса
params = {
    "figi": selected_figi,
    "from": from_datetime,
    "to": to_datetime,
    "interval": selected_interval,
    "instrumentId": selected_instrument_id
}

# Функция для получения данных
# @st.cache_data  # Кэширование данных для оптимизации
def fetch_data(api_url, params):
    response = requests.get(api_url, json=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Ошибка при получении данных: укажите правильно временной интервал или даты")
        return None

# Получение данных
data = fetch_data(API_URL, params)

if data is not None:
    st.subheader("Анализ цен с ShortSMA и LongSMA")

    # Получение данных
    total_prices_data = data.get("TotalPrices", None)
    short_sma_data = data.get("ShortSma", [])
    long_sma_data = data.get("LongSma", [])

    # Проверка наличия данных
    if short_sma_data and long_sma_data:
        # Если TotalPrices существует, выводим его как отдельное число
        if total_prices_data is not None:
            st.write(f"**Общая цена (TotalPrices):** {total_prices_data}")

        # Создание DataFrame для SMA
        sma_length = max(len(short_sma_data), len(long_sma_data))
        prices_df = pd.DataFrame({
            "Index": range(sma_length),
            "ShortSMA": short_sma_data + [None] * (sma_length - len(short_sma_data)),
            "LongSMA": long_sma_data + [None] * (sma_length - len(long_sma_data))
        })

        # Создание графика с Plotly
        fig = go.Figure()

        # Добавление ShortSMA
        fig.add_trace(go.Scatter(
            x=prices_df["Index"],
            y=prices_df["ShortSMA"],
            mode="lines",
            name="ShortSMA",
            line=dict(color="orange", dash="dot")
        ))

        # Добавление LongSMA
        fig.add_trace(go.Scatter(
            x=prices_df["Index"],
            y=prices_df["LongSMA"],
            mode="lines",
            name="LongSMA",
            line=dict(color="green", dash="dash")
        ))

        # Настройка внешнего вида графика
        fig.update_layout(
            title="График короткой и длинной скользящих средних (SMA)",
            xaxis_title="Индекс (X)",
            yaxis_title="Цена (Y)",
            showlegend=True,
            legend_title="Легенда",
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
        )

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных ShortSMA и LongSMA:")
        st.dataframe(prices_df)
    else:
        st.write("Нет данных для ShortSMA или LongSMA")


    st.markdown("""
    **Описание графика MDFA.Hq:**
    - Этот график отображает значения Hq, которые являются результатом многоразмерного фрактального анализа (MDFA).
    - Hq характеризует масштабирующуюся зависимость между различными частотами сигнала.
    - Высокие значения Hq указывают на более сложные зависимости в сигнале.
    """)

    # Визуализация MDFA.Hq
    hq_data = pd.DataFrame(list(data.get("MDFA", {}).get("Hq", {}).items()), columns=["Index", "Value"])

    if not hq_data.empty:


        # Создание графика с Plotly
        fig = px.line(
            hq_data,
            x="Index",
            y="Value",
            title="График MDFA.Hq (Индексы vs Значения)",  # Подпись графика
            labels={"Index": "Индекс", "Value": "Значение"},  # Подписи осей
            markers=True  # Добавляем маркеры (точки)
        )

        # Настройка внешнего вида графика
        fig.update_layout(
            xaxis_title="Индекс (X)",  # Подпись оси X
            yaxis_title="Значение (Y)",  # Подпись оси Y
            showlegend=True,
            legend_title="Легенда",
            margin=dict(l=50, r=50, t=80, b=50),  # Отступы вокруг графика
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")  # Шрифт
        )

        # Увеличиваем размер точек
        fig.update_traces(marker=dict(size=6, color="blue"), line=dict(color="green"))

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных MDFA.Hq:")
        st.dataframe(hq_data)  # Округление значений до 2 знаков после запятой
    else:
        st.write("Нет данных для MDFA.Hq")


    st.markdown("""
    **Описание графика MDFA.LogFq:**
    - Этот график отображает логарифмические спектры Fq, которые используются для анализа фрактальных свойств сигнала.
    - Каждая кривая на графике соответствует определенному значению q, которое влияет на вес различных частот в анализе.
    - LogFq помогает выявить масштабирующиеся свойства сигнала на разных временных шкалах.
    """)


    # Визуализация MDFA.LogFq
    st.subheader("MDFA.LogFq (все значения)")

    logfq_data = data.get("MDFA", {}).get("LogFq", {})
    if logfq_data:
        # Создаем датафрейм для всех значений
        combined_data = {}
        for key, values in logfq_data.items():
            combined_data[key] = values

        df_logfq = pd.DataFrame(combined_data)

        if not df_logfq.empty:
            # Устанавливаем индекс для DataFrame
            df_logfq.index = range(len(df_logfq))

            # Создание графика с Plotly
            fig = go.Figure()

            for column in df_logfq.columns:
                fig.add_trace(go.Scatter(
                    x=df_logfq.index,
                    y=df_logfq[column],
                    mode="lines+markers",
                    name=f"Логарифмический спектр {column}",
                    marker=dict(size=6),
                    line=dict(width=2)
                ))

            # Настройка внешнего вида графика
            fig.update_layout(
                title="График MDFA.LogFq (Все значения)",
                xaxis_title="Индекс (X)",
                yaxis_title="Логарифмическое значение (Y)",
                showlegend=True,
                legend_title="Каналы данных",
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
            )

            # Отображение графика
            st.plotly_chart(fig)

            # Показываем таблицу данных
            st.text("Таблица данных MDFA.LogFq:")
            st.dataframe(df_logfq)
        else:
            st.write("Нет данных для MDFA.LogFq")
    else:
        st.write("Нет данных для MDFA.LogFq")

    st.markdown("""
    **Описание графика MFSpectrum.Alpha:**
    - Alpha представляет собой мультифрактальный спектр, который характеризует степень сложности сигнала.
    - Значения Alpha зависят от параметра Q и показывают, как меняется фрактальная размерность при изменении масштаба.
    - Более широкий спектр Alpha указывает на большую сложность сигнала.
    """)

    # Визуализация MFSpectrum.Alpha
    st.subheader("MFSpectrum.Alpha")

    alpha_data = pd.DataFrame(data.get("MFSpectrum", {}).get("Alpha", []), columns=["Value"])
    alpha_data.index = data.get("MFSpectrum", {}).get("Qsorted", [])

    if not alpha_data.empty:
        # Создание графика с Plotly
        fig = px.line(
            alpha_data,
            x=alpha_data.index,
            y="Value",
            title="График MFSpectrum.Alpha (Мультифрактальный спектр α)",
            labels={"index": "Q-параметр", "Value": "Значение α"},
            markers=True
        )

        # Настройка внешнего вида графика
        fig.update_layout(
            xaxis_title="Q-параметр (X)",
            yaxis_title="Значение α (Y)",
            showlegend=True,
            legend_title="Легенда",
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
        )

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных MFSpectrum.Alpha:")
        st.dataframe(alpha_data)
    else:
        st.write("Нет данных для MFSpectrum.Alpha")

    st.markdown("""
    **Описание графика MFSpectrum.FAlpha:**
    - F(Alpha) является функцией плотности вероятности для различных значений Alpha.
    - Этот график помогает понять, какие значения Alpha наиболее распространены в сигнале.
    - Пики на графике F(Alpha) указывают на доминирующие масштабирующие режимы.
    """)

    # Визуализация MFSpectrum.FAlpha
    st.subheader("MFSpectrum.FAlpha")

    falpha_data = pd.DataFrame(data.get("MFSpectrum", {}).get("FAlpha", []), columns=["Value"])
    falpha_data.index = data.get("MFSpectrum", {}).get("Qsorted", [])

    if not falpha_data.empty:
        # Создание графика с Plotly
        fig = px.line(
            falpha_data,
            x=falpha_data.index,
            y="Value",
            title="График MFSpectrum.FAlpha (Функция F(α))",
            labels={"index": "Q-параметр", "Value": "F(α)"},
            markers=True
        )

        # Настройка внешнего вида графика
        fig.update_layout(
            xaxis_title="Q-параметр (X)",
            yaxis_title="F(α) (Y)",
            showlegend=True,
            legend_title="Легенда",
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
        )

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных MFSpectrum.FAlpha:")
        st.dataframe(falpha_data)
    else:
        st.write("Нет данных для MFSpectrum.FAlpha")


    st.markdown("""
    **Описание графика MFSpectrum.Tau:**
    - Tau(q) представляет собой масштабирующую функцию, которая используется для оценки фрактальных свойств сигнала.
    - Значения Tau(q) зависят от параметра q и показывают, как меняется масштабируемость при разных весах частот.
    - Линейная зависимость Tau(q) от q указывает на наличие однофрактальной структуры.
    """)

    # Визуализация MFSpectrum.Tau
    st.subheader("MFSpectrum.Tau")

    tau_data = pd.DataFrame(data.get("MFSpectrum", {}).get("Tau", []), columns=["Value"])
    tau_data.index = data.get("MFSpectrum", {}).get("Qsorted", [])

    if not tau_data.empty:
        # Создание графика с Plotly
        fig = px.line(
            tau_data,
            x=tau_data.index,
            y="Value",
            title="График MFSpectrum.Tau (Масштабирующая функция τ(q))",
            labels={"index": "Q-параметр", "Value": "τ(q)"},
            markers=True
        )

        # Настройка внешнего вида графика
        fig.update_layout(
            xaxis_title="Q-параметр (X)",
            yaxis_title="τ(q) (Y)",
            showlegend=True,
            legend_title="Легенда",
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
        )

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных MFSpectrum.Tau:")
        st.dataframe(tau_data)
    else:
        st.write("Нет данных для MFSpectrum.Tau")
        
    st.subheader("FDIAnalysis для всего большого интервала")

    fdi_analysis_data = data.get("FDIAnalysis", {})
    if fdi_analysis_data:
        # Обработка случая, если FDI является словарем
        if isinstance(fdi_analysis_data.get("FDI"), dict):
            # Извлекаем значение FDI из словаря
            fdi_analysis_data["FDI"] = fdi_analysis_data["FDI"]["Fdi"]

        # Преобразование данных в DataFrame для лучшего представления
        fdi_analysis_df = pd.DataFrame(list(fdi_analysis_data.items()), columns=["Parameter", "Value"])

        # Отображение таблицы данных
        st.text("Таблица данных FDIAnalysis:")
        st.dataframe(fdi_analysis_df.set_index("Parameter"))

        # Вывод описания каждого параметра
        st.markdown("""
        **Описание параметров FDIAnalysis:**
        - **Width**: Ширина сигнала, характеризующая разброс значений.
        - **Asym**: Асимметрия сигнала, показывающая степень неравенства положительных и отрицательных отклонений.
        - **Curvature**: Кривизна сигнала, характеризующая изменчивость формы сигнала.
        - **FDI**: Индекс фрактальной размерности, описывающий сложность сигнала.
        """)
    else:
        st.write("Нет данных для FDIAnalysis")


    st.markdown("""
    **Описание графика Window.FdiWind:**
    - Этот график отображает параметры FDI для каждого окна анализа.
    - Параметры включают Width (ширина сигнала), Asym (асимметрия), Curvature (кривизна) и Fdi (фрактальная размерность).
    - Изменения этих параметров во времени помогают выявить динамические изменения сложности сигнала.
    """)

        # Визуализация Window.FdiWind
    st.subheader("Window.FdiWind")

    fdi_wind_data = data.get("Window", {}).get("FdiWind", [])
    if fdi_wind_data:
        # Преобразование списка словарей в DataFrame
        fdi_wind_df = pd.DataFrame(fdi_wind_data)
        fdi_wind_df.index = range(len(fdi_wind_data))

        # Создание графиков для каждого параметра FdiWind
        for column in ["Width", "Asym", "Curvature", "Fdi"]:
            fig = px.line(
                fdi_wind_df,
                x=fdi_wind_df.index,
                y=column,
                title=f"График Window.FdiWind - {column}",
                labels={"index": "Индекс", "value": column},
                markers=True
            )

            # Настройка внешнего вида графика
            fig.update_layout(
                xaxis_title="Индекс (X)",
                yaxis_title=f"{column} (Y)",
                showlegend=False,
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
            )

            # Отображение графика
            st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных Window.FdiWind:")
        st.dataframe(fdi_wind_df)
    else:
        st.write("Нет данных для Window.FdiWind")



    st.markdown("""
    **Описание графика Window.HurstWind:**
    - Hurst показывает степень долгосрочной памяти в сигнале для каждого окна анализа.
    - Значения Hurst близкие к 0.5 указывают на случайный процесс.
    - Значения Hurst > 0.5 указывают на трендовость (персистентность), а < 0.5 — на антиперсистентность.
    """)

    # Визуализация Window.HurstWind
    st.subheader("Window.HurstWind")

    hurst_wind_data = data.get("Window", {}).get("HurstWind", [])
    if hurst_wind_data:
        hurst_wind_df = pd.DataFrame(hurst_wind_data, columns=["Value"])
        hurst_wind_df.index = range(len(hurst_wind_data))

        # Создание графика с Plotly
        fig = px.line(
            hurst_wind_df,
            x=hurst_wind_df.index,
            y="Value",
            title="График Window.HurstWind",
            labels={"index": "Индекс", "Value": "Значение"},
            markers=True
        )

        # Настройка внешнего вида графика
        fig.update_layout(
            xaxis_title="Индекс (X)",
            yaxis_title="Значение HurstWind (Y)",
            showlegend=False,
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Arial, monospace", size=12, color="#7f7f7f")
        )

        # Отображение графика
        st.plotly_chart(fig)

        # Отображение таблицы данных
        st.text("Таблица данных Window.HurstWind:")
        st.dataframe(hurst_wind_df)
    else:
        st.write("Нет данных для Window.HurstWind")