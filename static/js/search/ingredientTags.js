$(document).ready(function () {

  // Ingredient names will be saved
  let includeIngredients = [];
  let excludeIngredients = [];

  // Recognize ingredients from url parameters, in hiddent inputs
  if ($("#include-ingredient-names").val() !== "") {
    includeIngredients = $("#include-ingredient-names").val().split(",");
  }
  if ($("#exclude-ingredient-names").val() !== "") {
    excludeIngredients = $("#exclude-ingredient-names").val().split(",");
  }

  // Put tags for recognized ingredients
  for (let ingredient of includeIngredients) {
    putTag(ingredient, $("#include-input"));
  }
  for (let ingredient of excludeIngredients) {
    putTag(ingredient, $("#exclude-input"));
  }

  setPlaceholder();

  // Add ingredient tag when a comma is typed in an ingredient input
  $(".ingredient-input").bind('change keyup', function () {
    setTags($(this));
  });

  // Focus on input even when the big area is clicked
  $(".tags-area").click(function() {
    $(this).children("input").focus();
  });

  // Delete tags when backspace is pressed
  $(".ingredient-input").keydown(function(e) {
    if (e.which == 8 && $(this).val() === "") {
      $(this).prev().remove();
      if ($(this).attr("id") == "include-input") {
        includeIngredients.pop();
      } else if ($(this).attr("id") == "exclude-input") {
        excludeIngredients.pop();
      }
      setIngredientValues();
      setPlaceholder();
    }
  });

  function setTags(inputField) {
    // Set tags if one or more ingredients are typed separated by comma
    while (inputField.val().includes(",")) {
      let inputValue = inputField.val();
      let commaPosition = inputValue.indexOf(",");
      inputValue = inputField.val().slice(0, commaPosition).toLowerCase();
      let remainingValue = inputField.val().slice(commaPosition+1).toLowerCase();
      inputField.val(remainingValue);
      if (inputValue) {
        putTag(inputValue, inputField)
        saveIngredient(inputValue, inputField)
      }
    }
    setIngredientValues();
    setPlaceholder();
  };

  function putTag(inputValue, inputField) {
    // Put a tag containing inputValue before inputField
    let tag = "<div class='tag-container'><span class='badge'>"
      + inputValue + "</span></div>";
    inputField.before(tag);
    $(".input-remaining-space").css("width", "50%");
  };

  function saveIngredient(inputValue, inputField) {
    // Push ingredient to corresponding array
    if (inputField.attr("id") == "include-input") {
      includeIngredients.push(inputValue);
    } else if (inputField.attr("id") == "exclude-input") {
      excludeIngredients.push(inputValue);
    }
  };

  function setIngredientValues() {
    // Set values at hidden inputs with ingredient names
    $("#include-ingredient-names").val(includeIngredients.join(","));
    $("#exclude-ingredient-names").val(excludeIngredients.join(","));
  };

  function setPlaceholder() {
    // Set placeholder at inputs corresponding to igredients
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
  };

});