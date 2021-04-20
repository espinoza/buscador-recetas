$(document).ready(function () {

  $("#search-input").bind('change keyup', function (e) {
    if ($(this).val().includes(",")) {
      let inputValue = $(this).val();
      let commaPosition = inputValue.indexOf(",");
      inputValue = $(this).val().slice(0, commaPosition);
      $(this).val("");
      let tag = "<span class='badge bg-primary mx-1'>" + inputValue + "</span>";
      $(this).before(tag);
      let ingredientNames = $("#ingredient-names").val() + inputValue + ",";
      $("#ingredient-names").val(ingredientNames);
    }
  });

  $("#input-area").click(function() {
    $("#search-input").focus();
  });

  $("#search-input").keydown(function(e) {
    if (e.which == 8 && $(this).val() === "") {
      $(this).prev().remove();
    }
  });

});
