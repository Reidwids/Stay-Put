function previewImages() {

    var preview = document.querySelector('#preview');
    
    if (this.files) {
      [].forEach.call(this.files, readAndPreview);
    }
  
    function readAndPreview(file) {
  
      var reader = new FileReader();
      
      reader.addEventListener("load", function() {
        var image = new Image();
        image.width = 250;
        image.title  = file.name;
        image.src    = this.result;
        preview.appendChild(image);
      });
      
      reader.readAsDataURL(file);
      
    }
  
  }
  
  document.querySelector('#file-input').addEventListener("change", previewImages);