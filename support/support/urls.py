from typing import Callable
import string
import random

# from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpRequest

def create_random_string(size: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(size))

content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request rates</title>
    <link 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
        rel="stylesheet" 
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" 
        crossorigin="anonymous"
    />
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <script>
        $(document).ready(function () {
            $("#makeRequest").click(function () {
                const data = {
                    src_currency: "USD",
                    dest_currency: "EUR",
                };
                $.ajax({
                    url: "http://127.0.0.1:8000/rate-check/",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(data),
                    success: function (response) {
                        console.log("Success:", response);
                        $("#output").text(JSON.stringify(response, null, 2));
                    },
                    error: function (xhr, status, error) {
                        console.error("Error:", error);
                        $("#output").text("Error occurred: " + error);
                    }
                });
            });
            $("#generate").click(function () {
                $.ajax({
                    url: "http://localhost:8000/generate-article",
                    type: "GET",
                    success: function(data) {
                        const newItem = `<tr>
                            <td>${data.title}</td>
                            <td>${data.description}</td>
                        </tr>`;
                        $("#article-ideas").append(newItem);
                    },
                    error: function (jqdata, status, error) {
                        console.log(error);
                        alert("An error occured while generating an article idea.")
                    },
                });
            });
        
        });
    </script>


    <h1>Request rates</h1>
    <button id="generate" class="btn btn-danger">Fetch information</button>
    <button id="makeRequest" class="btn btn-primary">Request a rate</button>
    <pre id="output"></pre>

    <table class="table table-striped">
        <tr>
            <th>Title</th>
            <th>Description</th>
        </tr>
        <tbody id="article-ideas"></tbody>

    <br/>

    </table>
</body>
</html>
"""

def generate_article_idea(request: HttpRequest)-> HttpResponse:
    return HttpResponse(content)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(route="generate-article", view=generate_article_idea),
]
