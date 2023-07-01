$(document).ready(function () {
    $("#avatar-img").change(function () {
        var reader = new FileReader();
        reader.onload = function (event) {
            $("#avatar-show").attr("src", event.target.result);
        };
        reader.readAsDataURL($("#avatar-img").prop("files")[0]);
    });
});
