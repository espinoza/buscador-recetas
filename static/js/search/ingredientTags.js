$(document).ready(function () {

  let includeIngredients = [];
  let excludeIngredients = [];
  setPlaceholder();

  $(".ingredient-input").bind('change keyup', function () {
    // Add ingredient tag when input contains a comma
    if ($(this).val().includes(",")) {
      let inputValue = $(this).val();
      let commaPosition = inputValue.indexOf(",");
      inputValue = $(this).val().slice(0, commaPosition);
      $(this).val("");
      if (inputValue) {
        let tag = "<div class='tag-container'><span class='badge'>"
          + inputValue + "</span></div>";
        $(this).before(tag);
        $(".input-remaining-space").css("width", "50%");
        if ($(this).attr("id") == "include-input") {
          includeIngredients.push(inputValue);
        } else if ($(this).attr("id") == "exclude-input") {
          excludeIngredients.push(inputValue);
        }
        setValues();
        setPlaceholder();
      }
    }
  });

  $(".tags-area").click(function() {
    $(this).children("input").focus();
  });

  $(".ingredient-input").keydown(function(e) {
    // Delete tags when backspace is pressed
    if (e.which == 8 && $(this).val() === "") {
      $(this).prev().remove();
      if ($(this).attr("id") == "include-input") {
        includeIngredients.pop();
      } else if ($(this).attr("id") == "exclude-input") {
        excludeIngredients.pop();
      }
      setValues();
      setPlaceholder();
    }
  });

  function setValues() {
    $("#include-ingredient-names").val(includeIngredients.join(","));
    $("#exclude-ingredient-names").val(excludeIngredients.join(","));
  }

  function setPlaceholder() {
    if (includeIngredients.length == 0) {
      $("#include-input").attr("placeholder", "Incluir ingredientes");
    } else {
      $("#include-input").attr("placeholder", "");
    }
    if (excludeIngredients.length == 0) {
      $("#exclude-input").attr("placeholder", "Excluir ingredientes");
    } else {
      $("#exclude-input").attr("placeholder", "");
    }
  }

});
