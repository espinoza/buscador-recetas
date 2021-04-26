$(document).ready(function () {

  let ingredientText = $('#ingredient-section').text();
  spanish_regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/

  $(document).mouseup(updateForm);
  // $(document).on('mouseup', '#ingredient-section', getSelectedText);
  // $('#ingredient-section').mouseup(getSelectedText);

function getSelectedText() {
  let selectedText = "";
  if (window.getSelection) {
    selectedText = window.getSelection().toString();
  } else return;
  return selectedText;
}

function selectionIngredient() {
  let text = getSelectedText()
  if (ingredientText.includes(text) && spanish_regex.test(text)) {
    return text;
  }
  return false
}

function updateForm() {
  ingredient = selectionIngredient()
  if (ingredient) {
    $('#btn-add').attr('disabled', false);
    $('#btn-add').removeClass('btn-secondary').addClass('btn-primary');
    $('#new-ingredient').attr('value', ingredient); 
  } else {
    $('#btn-add').attr('disabled', true);
    $('#btn-add').removeClass('btn-primary').addClass('btn-secondary');
    $('#new-ingredient').attr('value', "");
  }
}

});