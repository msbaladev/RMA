from io import BytesIO
from django.urls import reverse
from django.shortcuts import render,redirect
from django.http import FileResponse, HttpResponse, JsonResponse

from RMA.templatetags.rma_tags import *
from .models import *
from django.core.paginator import Paginator
import pandas as pd


def home(request):
    quarter = Current_quarter()
    return redirect(reverse("dashboard", kwargs={"quarter": quarter}))



def dashboard(request, quarter):
    data = rma_file.objects.filter(quarter=quarter).values()
    print(data, "ppp")
    print(Current_quarter)
    paginator = Paginator(data, 10)  # Show 10 books per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # return render(request, 'main.html', {'page_obj': page_obj})
    print(quarter, "]][]][  ]")
    return render(request, "index.html", {"quarter": quarter, "data": page_obj})


# def home(request):
#     quarter=Current_quarter()
#     print(quarter)
#     return render(request, 'index.html')


def file_upload(request,quarter):

    try:
        if request.method == "POST":
            file = request.FILES["file"]
          
            data = pd.read_excel(file, engine="openpyxl")

            data.fillna("0", inplace=True)
            # data.dropna(subset=['Site', 'PN'],how='any',inplace=True)

            # data=data.replace({np.NaN: None})
            # delete= icc_quanta.objects.filter(quarter = quarter).delete()
            row_iter = data.iterrows()
           
            bulk_update = []
            for index, row in row_iter:
             
                rma_data = rma_file(
                    quarter=quarter,
                    item=row["Item"],
                    pn=row["PN"],
                    description=row["Description"],
                    qty=row["Qty"],
                    usd=row["Rework fee(USD)"],
                    scrap=row["Scrap Material"],
                    unit_freight=row["Unit Freight (USD)"],
                    unit_price=row["Unit  price (USD)"],
                    ext_price=row["Ext price (USD)"],
                    remark=row["Remark"],
                )
                rma_data.save()
            return redirect("/")
    except:
        return JsonResponse({"status": "something went wrong!!!!!!!"})





def download_Iness_bulkapproval(request, quarter):
    columns = [
        "item",
        "quarter",
        "pn",
        "description",
        "qty",
        "usd",
        "scrap",
        "unit_freight",
        "unit_price",
        "ext_price",
        "remark",
        "status",
        "approval_comments",
    ]
    alias = [
        "item",
        "quarter",
        "pn",
        "description",
        "qty",
        "usd",
        "scrap",
        "unit_freight",
        "unit_price",
        "ext_price",
        "remark",
        "status",
        "approval_comments",
    ]

    with BytesIO() as b:
        with pd.ExcelWriter(b, engine="xlsxwriter") as writer:
            data = rma_file.objects.filter(quarter=quarter).values_list(*columns)
            print(data, "++++++", quarter)
            df = pd.DataFrame(data, columns=columns)

            df.to_excel(writer, index=False, header=alias, sheet_name="Sheet1")

            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            money_format = workbook.add_format({"num_format": "$#,##0.0000"})

            header_format_3 = workbook.add_format(
                {
                    "bold": True,
                    "text_wrap": True,
                    "valign": "top",
                    "fg_color": "green",
                    "color": "white",
                    "border": 1,
                }
            )

            # Apply the header format
            for col_num in range(len(alias)):
                if alias[col_num] in ["status", "approval_comments"]:
                    worksheet.write(0, col_num, alias[col_num], header_format_3)
                else:
                    worksheet.write(0, col_num, alias[col_num])

            # Apply data validation for the "status" column
            worksheet.data_validation(
                "L2:L1048576", {"validate": "list", "source": ["Approved", "Rejected"]}
            )

        response = HttpResponse(b.getvalue(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'inline; filename="RMA InESS Bulk upload All Parts.xlsx"'
        )
        return response






def RMA_iness_bulk_upload(request, quarter):

    file = request.FILES["rma_bulk_file"]
    qp_data = rma_file.objects.filter(quarter=quarter)
    # df = pd.read_excel(excel)

    data = pd.read_excel(file)
    data.fillna("", inplace=True)

    for qp in qp_data:

        # df = data.replace({0: None, 'nan': ''})
        partnumber = data[(data["pn"] == qp.pn) & (data["quarter"] == qp.quarter)]

        approval_status = ""
        comments = ""

        if not partnumber.empty:
            iness_approval_status = partnumber["status"].values[0]
            iness_comments = partnumber["approval_comments"].values[0]

            # Convert NaN values to empty strings
            approval_status = (
                "" if pd.isna(iness_approval_status) else str(iness_approval_status)
            )
            comments = "" if pd.isna(iness_comments) else str(iness_comments)

        # Update the database with the retrieved values
        rma_data = rma_file.objects.filter(id=qp.id, quarter=quarter).update(
            status=approval_status, approval_comments=comments
        )

    return redirect("/")