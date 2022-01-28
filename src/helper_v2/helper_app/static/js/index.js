(function () {
  document.querySelector('#tagInput').addEventListener('keydown', tagInput);
  function tagInput(e) {
    if (e.keyCode != 13) {
      return;
    }

    e.preventDefault();

    let tagName = this.value;
    this.value = '';
    addNewTag(tagName);
    updateTagsString();
  }

  function addNewTag(name) {
    let tagsContainer = document.querySelector('#tagsContainer');
    if (name == ' ') {
      return;
    }
    let tagsMarkup = `
      <li class="tag">
        <span class="name">${name}</span>
        <span onClick="removeTag(this)" class="btnRemove bold cursor red-text del-tag">X</span>
      </li>
          `;
    tagsContainer.insertAdjacentHTML('beforeend', tagsMarkup);
  }
})();

function fetchTagArray() {
  let tags = [];
  let tagsArray = document.querySelectorAll('.tag');
  tagsArray.forEach(e => {
    nameItem = e.querySelector('.name').innerHTML;
    if (nameItem === '') {
      return;
    }
    tags.push(nameItem);
  });
  return tags;
}

function updateTagsString() {
  let tagsArray = fetchTagArray();
  let tagsString = document.querySelector('input[name="tagsString"]');
  tagsString.value = tagsArray.join(',');
}

function removeTag(e) {
  e.parentElement.remove();
  updateTagsString();
}
