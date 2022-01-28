(function () {
  document.querySelector('#categoryInput').addEventListener('keydown', CategoryInput);
  function CategoryInput(e) {
    if (e.keyCode != 13) {
      return;
    }

    e.preventDefault();

    let categoryName = this.value;
    this.value = '';
    addNewCategory(categoryName);
    updateCategoriesString();
  }

  function addNewCategory(name) {
    let categoriesContainer = document.querySelector('#categoriesContainer');
    if (name == ' ') {
      return;
    }
    let categoriesMarkup = `
      <li class="category">
        <span class="name">${name}</span>
        <span onClick="removeCategory(this)" class="btnRemove bold">X</span>
      </li>
          `;
    categoriesContainer.insertAdjacentHTML('beforeend', categoriesMarkup);
  }
})();

function fetchCategoryArray() {
  let categories = [];
  let categoriesArray = document.querySelectorAll('.category');
  categoriesArray.forEach(e => {
    nameItem = e.querySelector('.name').innerHTML;
    if (nameItem === '') {
      return;
    }
    categories.push(nameItem);
  });
  return categories;
}

function updateCategoriesString() {
  let categoriesArray = fetchCategoryArray();
  let categoriesString = document.querySelector('input[name="categoriesString"]');
  categoriesString.value = categoriesArray.join(',');
}

function removeCategory(e) {
  e.parentElement.remove();
  updateCategoriesString();
}

let elem = document.querySelector('.modal');
let instance = M.Modal.init(elem);
