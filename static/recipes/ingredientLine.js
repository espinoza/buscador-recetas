$(document).ready(function () {

  let idIngredients = [];
  let numberOfIngredientLines = $(".ingredient-line").length;
  for (let i = 1; i <= numberOfIngredientLines; i++) {
    idIngredients.push(i);
  };
  let lastAddedId = idIngredients[idIngredients.length - 1];

  $(document).on('click', '.add-ingredient-line', function() {
    let tagId = $(this).attr("id");
    let idNumber = parseInt(tagId.slice(tagId.search("-") + 1));
    let newId = lastAddedId + 1;
    lastAddedId += 1;
    if (idNumber > 0) {
      let newPosition = idIngredients.indexOf(idNumber);
      idIngredients.splice(newPosition, 0, newId);
    } else if (idNumber == 0) {
      idIngredients.push(newId);
    };
    $(this).parent().before(getNewLine(newId));
    $("#ingredientline-" + newId).focus();
    $("#number-of-ingredients").attr("value", idIngredients.length);
  });

  $(document).on('keypress', '.ingredient-line', function(e) {
    let keyCode = e.keyCode || e.which;
    if (keyCode == 13) {
      let tagId = $(this).attr("id");
      let idNumber = parseInt(tagId.slice(tagId.search("-") + 1));
      let position = idIngredients.indexOf(idNumber);
      let idButton = 0;
      if (position < idIngredients.length - 1) {
        idButton = idIngredients[position + 1];
      };
      e.preventDefault();
      $("#addline-" + idButton).click();
    };
  });

  $(document).on('click', '.remove-ingredient-line', function() {
    let tagId = $(this).attr("id");
    let idNumber = tagId.slice(tagId.search("-") + 1);
    let newIdIngredients = idIngredients.filter(e => e != idNumber);
    idIngredients = newIdIngredients;
    $(this).parent().remove();
    $("#number-of-ingredients").attr("value", idIngredients.length);
  });

});

function getNewLine(id) {
  let buttons = getButton(id, "remove") + ' ' + getButton(id, "add");
  return '<p id="line-' + id + '">' + getNewInput(id) + ' ' + buttons + '</p>';
};

function getNewInput(id) {
  let inputId = 'id="ingredientline-' + id + '" ';
  let inputName = 'name="ingredient_line_' + id + '" ';
  let inputClass = 'class="ingredient-line" ';
  return '<input ' + inputId + inputName + inputClass + 'type="text">';
};

function getButton(id, action) {
  let bsClass = '';
  let sign = '';
  if (action == "remove") {
    bsClass = "bg-danger";
    sign = "-";
  } else if (action == "add") {
    bsClass = "bg-success";
    sign = "+";
  };
  let buttonClass = action + '-ingredient-line badge ' + bsClass;
  let buttonId = action + 'line-' + id;
  let openTag = '<span id="' + buttonId + '" class="' + buttonClass + '">';
  let closeTag = '</span>';
  return openTag + sign + closeTag;
};
