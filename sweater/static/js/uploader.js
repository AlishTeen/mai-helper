files = document.querySelector('#files')
fileTemplate = document.querySelector('#fileTemplate')

upd = $("#dnd-zone").dmUploader({
  url: '/api/submit/file',
  dnd: true,
  multiple: true,
  maxFileSize: 16777216,

  onDragEnter: function(){
      this.addClass('active');
    },

  onDragLeave: function(){
      this.removeClass('active');
    },

  onNewFile: function (id, file){
    let newFile = fileTemplate.content.cloneNode(true)
    newFile.querySelector(".file").id = `file-${id}`
    newFile.querySelector("h5").textContent = file.name
    files.appendChild(newFile)

  },

  onUploadProgress: function (id, percent) {
    document.querySelector(`#file-${id}`).children[1].textContent = `${percent}%`
  }
})
