#!/usr/bin/env python3

unicode_internal_encode: 'utf-8'

import urllib.request
from datetime import datetime
from decimal import *

reportheader = """<!DOCTYPE html> 
                    <html> 
                        <meta charset="UTF-8">
                        <title>SEO Report</title>
                    <!-- <link rel="stylesheet" href="reporter_master.css"> -->
                        <body bgcolor="lightgray"> 
                            <font face="verdana,arial,sans-serif">
                            </font> 
                                <h2 align=center> 
                                    <strong><u>SEO Url Validation Report</u></strong> 
                                </h2> 
                            <br> 
                            <table border=1px style:"width:auto" cellpadding=0 cellspacing=0>
                                <h3 align=left>
                                    <strong><u> Overall Summary: </u></strong>
                                </h3>
                                <tr> 
                                    <td align=center width=20% ><strong> Total URLs </strong></td> 
                                    <td align=center width=20%><strong> Total Response Time</strong></td> 
                                    <td align=center width=20%><strong> Average Response Time</strong></td>
                                    <td align=center width=20%><strong>Environment</strong></td> 
                                    <td align=center width=20%><strong>Total Redirected URLs </strong></td> 
                                </tr>
                """

reportdata = """<table border=1px style:"width:auto" cellpadding=0 cellspacing=0>
                    <h3 align=left>
                        <strong><u> Detailed Breakup: </u></strong>
                    </h3>
                    <tr background-color=solid black align=center> 
                        <td width=20%><strong>Url</strong></td> 
                        <td width=20%><strong>Redirected_Url</strong></td> 
                        <td width=5%><strong>Http Code</strong></td> 
                        <td width=5%><strong>Status</strong></td> 
                        <td width=5%><strong>Response Time(ms)</strong> </td 
                    </tr>
            """

# Initialization

input_file = open("urls.txt", "r")
output_file = open('report.html', 'w')
output_file.write(reportheader)
output_file.write("<br>")
Environment = ""
total_failed_URLs = 0
total_URLs = 0
getcontext().prec = 3
total_response_time = 0
row_content_global = ""

for uri in input_file:

# Checks the Url environment

    if "stag" in uri:
        Environment = "Stage"
    elif "dev" in uri:
        Environment = "Dev"
    else:
        Environment = "Production"

    total_URLs = total_URLs + 1
    row_content = ""
    row_content += "<tr>"

# Response time calculation

    first_hour = datetime.now().hour
    first_min = datetime.now().minute
    first_sec = datetime.now().second
    first_microsec = datetime.now().microsecond
    uri = uri.strip('\n')
    response = urllib.request.urlopen(uri)
    second_hour = datetime.now().hour
    second_minute = datetime.now().minute
    second_second = datetime.now().second
    second_microsec = datetime.now().microsecond
    response_time = 0
    average_response_time = 0
    redirect_url = "Url not redirected"

    if response.geturl() == uri:
        row_content += "<td align=center>"
        row_content += uri
        row_content += "</td>"
        row_content += "<td align=center>"
        row_content += redirect_url
        row_content += "</td>"
    else:
        total_failed_URLs = total_failed_URLs + 1
        row_content += "<td align=center>"
        row_content += uri
        row_content += "</td>"
        row_content += "<td align=center>"
        row_content += response.geturl()
        row_content += "</td>"

    row_content += "<td align=center>"
    row_content += str(response.code)
    row_content += "</td>"

# HTTP status check
    if response.code == 200:
        row_content += "<td align=center>"
        row_content += "Success"
    else:
        row_content += "<td align=center bgcolor=red>"
        row_content += "Failure"
        row_content += "</td>"

    if second_hour == first_hour:
        response_time = response_time + 60 * int(str(second_minute - first_min))
        response_time = response_time + second_second - first_sec

    else:
        response_time = 60 * (second_minute + 60 - first_min)
        response_time = response_time + second_second - first_sec

    response_time = response_time * 1000.0
    getcontext().prec = 3
    response_time += (second_microsec - first_microsec) * pow(10, -3)
    total_response_time += response_time
    response_time = ("%.3f" % response_time)
    print((second_microsec - first_microsec) * pow(10, -3))
    row_content += "<td  align=center>"
    row_content += str(response_time)
    row_content += "</td>"
    row_content += "</tr>"

row_content_global += row_content

# Calculating average response time
average_response_time = total_response_time / total_URLs

row_value = "<tr>"
row_value += "<td align=center>"
row_value += str(total_URLs)
row_value += "</td>"

total_response_time /= 1000
total_response_time = ("%.3f" % total_response_time)
row_value += "<td align=center>"
row_value += str(total_response_time)
row_value += "</td>"

average_response_time = ("%.3f" % average_response_time)
row_value += "<td align=center>"
row_value += str(average_response_time)
row_value += "</td>"

row_value += "<td align=center>"
row_value += Environment
row_value += "</td>"

row_value += "<td align=center>"
row_value += str(total_failed_URLs)
row_value += "</td>"

row_value += "</tr>"
row_value += "</table>"

output_file.write(row_value)

output_file.write("<br>")

output_file.write(reportdata)

output_file.write(row_content_global)

output_file.write("</table>")
output_file.write("</body>")
output_file.write("</html>")

# Close the file
input_file.close()
output_file.close()
