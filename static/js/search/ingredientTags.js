$(document).ready(function () {

  let includeIngredients = [];
  let excludeIngredients = [];

  $(".ingredient-input").bind('change keyup', function () {
    if ($(this).val().includes(",")) {
      let inputValue = $(this).val();
      let commaPosition = inputValue.indexOf(",");
      inputValue = $(this).val().slice(0, commaPosition);
      $(this).val("");
      let tag = "<span class='badge'>"
                + inputValue + "</span>";
      $(this).before(tag);
      if ($(this).attr("id") == "include-input") {
        includeIngredients.push(inputValue);
      } else if ($(this).attr("id") == "exclude-input") {
        excludeIngredients.push(inputValue);
      }
      setValues();
    }
  });

  $(".tags-area").click(function() {
    $(this).children("input").focus();
  });

  $(".ingredient-input").keydown(function(e) {
    if (e.which == 8 && $(this).val() === "") {
      $(this).prev().remove();
      if ($(this).attr("id") == "include-input") {
        includeIngredients.pop();
      } else if ($(this).attr("id") == "exclude-input") {
        excludeIngredients.pop();
      }
      setValues();
    }
  });

  function setValues() {
    $("#include-ingredient-names").val(includeIngredients.join(","));
    $("#exclude-ingredient-names").val(excludeIngredients.join(","));
  }

});
