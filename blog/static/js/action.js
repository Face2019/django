
/*
$("[data-next-modal-photo]").click(function () {
    modalPhotoIndex = (modalPhotoIndex +1) % numberOfModalPhotos;
    var modalPhotoSource = $("[data-example-part-of-face=" + modalPartOfFace + "]").find("[data-example-face=" + modalPhotoIndex + "]").find("[data-face-id]").attr("src");
    var modalPhotoDescripton = $("[data-example-part-of-face=" + modalPartOfFace + "]").find("[data-example-face=" + modalPhotoIndex + "]").find("[data-choose-example-face]").text();

    $("[data-modal-photo]").attr("src", modalPhotoSource);
    $("[data-modal-photo-desc]").text(modalPhotoDescripton);
});

$("[data-prev-modal-photo]").click(function () {
    if (modalPhotoIndex == 0){
        modalPhotoIndex = numberOfModalPhotos -1;
    } else{
        modalPhotoIndex = (modalPhotoIndex - 1)% numberOfModalPhotos;
    }
    var modalPhotoSource = $("[data-example-part-of-face=" + modalPartOfFace + "]").find("[data-example-face=" + modalPhotoIndex + "]").find("[data-face-id]").attr("src");
    var modalPhotoDescripton = $("[data-example-part-of-face=" + modalPartOfFace + "]").find("[data-example-face=" + modalPhotoIndex + "]").find("[data-choose-example-face]").text();

    $("[data-modal-photo]").attr("src", modalPhotoSource);
    $("[data-modal-photo-desc]").text(modalPhotoDescripton);

});
*/

// dodać pierwszy element potem reszta
//asynchroniczny AJAX

function createDivWithExampleFaces(partOfFaces,exampleFacesData){

    var divData = '<div data-example-part-of-face="' + partOfFaces +
                  '" class="row justify-content-around h-100 align-items-center"' +
                  'style="white-space: nowrap; text-align: center; display:none;">';

    for (var i in exampleFacesData) {
        var photoData = exampleFacesData[i];
        if (i == 0){
            divData += '<div data-example-face='+ i +' class="col-12 h-100" style="text-align: center;">';
        }else{
            divData += '<div data-example-face='+ i + ' class="col-12 h-100" style="display: none;text-align: center;">';
        }
        divData += '<div class="row h-100 align-items-center">' +
                        '<div class="col-8 h-90" style="text-align: center;  display: flex;align-items: center;justify-content: center;">' +
                             '<img data-face-id=' + photoData["id"]+ ' style="max-height: 100%;max-width: 100%;" class="rounded-circle" src="' + photoData["source"] +'">' +
                        '</div>' +
                        '<div class="col-3 h-90">' +
                            '<div class="row justify-content-around h-100 align-items-center">' +
                                '<p class="col-10" style="color: white">' + photoData["name"] + '</p>' +
                                '<button data-zoom class="col-10 choose-buton btn btn-outline-dark">ZOOM IN</button>' +
                                '<button data-choose-part-of-face class="col-10 choose-buton btn btn-outline-dark">CHOOSE</button>' +
                              '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';

    }
    divData += '</div>';
    return divData;
}

function downloadExampleFaces(partOfFace){

    if (!downloadedPartsOfFace[partOfFace]){
        return $.post(LOAD_FACES_URL, {"partOfFace": partOfFace});
    }
    return null;
}

$buttonPartOfFace.click(function () {
    var partOfFace = $(this).data("part-of-face");
    $.when(downloadExampleFaces(partOfFace)).done(function(res){
        if (res){
            var divWithExampleFaces = createDivWithExampleFaces(partOfFace, res["example_faces"]);
            $exampleFacesDiv.append(divWithExampleFaces);
            downloadedPartsOfFace[partOfFace] = true;
        }
        activePartOfFace = partOfFace;
        $("[data-example-part-of-face]").hide();
        $acitveExampleFaces = $("[data-example-part-of-face=" + activePartOfFace + "]");
        $acitveExampleFaces.show();
        numberOfExampleFaces = $acitveExampleFaces.find("[data-example-face]").length;
        $buttonPartOfFace.removeClass("choose-button-block" );
        $("[data-part-of-face=" + activePartOfFace + "]").addClass("choose-button-block");
        $chosenPartOfFace.attr('src', defaultImageSourceOfTheChosenFace);
        exampleFacexIndex = 0;
        $acitveExampleFaces.find("[data-example-face]").hide();
        $acitveExampleFaces.find("[data-example-face=" + exampleFacexIndex + "]").show();
    });

});


$chooseExamplFace.click(function () {
    $chooseExamplFace.each(function() {
        $(this).parent().find("[data-face-id]").removeClass("example-face-border");
    });
    $(this).parent().find("[data-face-id]").addClass("example-face-border");
});

$imagesShowingExampleFaces.click(function () {
    numberOfModalPhotos = $(this).parent().parent().parent().parent().find("[data-example-face]").length;
    modalPartOfFace =  $(this).parent().parent().parent().parent().data('example-part-of-face');
    modalPhotoIndex = $(this).parent().parent().parent().data("example-face");
    $("[data-chose-example-face-modal]").modal('show');
    $("[data-modal-photo]").attr("src", $(this).attr("src"));
    var nameOfTheExampleFace = $(this).parent().parent().find("[data-choose-example-face]").text();
    $("[data-modal-photo-desc]").text(nameOfTheExampleFace);
});

$nextFace.click(function(){
    exampleFacexIndex = (exampleFacexIndex+1) % numberOfExampleFaces;
    $acitveExampleFaces.find("[data-example-face]").hide();
    $acitveExampleFaces.find("[data-example-face=" + exampleFacexIndex + "]").show();
});

$previousFace.click(function(){
    exampleFacexIndex = (numberOfExampleFaces + (exampleFacexIndex-1)) % numberOfExampleFaces;
    $acitveExampleFaces.find("[data-example-face]").hide();
    $acitveExampleFaces.find("[data-example-face=" + exampleFacexIndex + "]").show();
    console.log(exampleFacexIndex);
    console.log("ZOOM PHOOTOOO");
    console.log($zoomPhoto);

});

$(document).on("click", "[data-choose-part-of-face]", function() {
    console.log("ACTIVE");
    var $activeExampleFace = $acitveExampleFaces.find("[data-example-face=" + exampleFacexIndex + "]").find("[data-face-id]");
    $chosenPartOfFace.attr('src', $activeExampleFace.attr('src'));

    activeExamplePhotoConfig["faceId"] = $activeExampleFace.data("face-id");
});

$(document).on("click", "[data-zoom]", function() {
    $modalWithExampleFace.show();
    console.log($(this));
    //console.log("ZOOM PHOOTOOO");
    //console.log("ZOOM PHOOTOOO");
});


$( "#main-input" ).change(function() {
    var reader = new FileReader();
    var fileData = $(this)[0].files[0];
    console.log($(this)[0].files[0]);
    reader.readAsDataURL(fileData);
    reader.onload = function ()
    {
       $userInputPhoto.attr("src", reader.result);
    };
});
function disableWholeScreen(){
    $preloadContainer.css("z-index", 999);
    $body.addClass('grey-scale');
    $body.find('img').shiningImage();
    $body.children().addClass('disabled');
}
function enableWholeScreen(){
    $body.removeClass('grey-scale');
    var $images = $body.find('img');
    var idx;
    for (idx = 0; idx < $images.length; idx+=1) {
        $($images[idx]).data("shiningImage").stopshine();
        $($images[idx]).siblings( "#undefined_canvas" ).remove();
    }
    $body.find('img').show();
    $body.children().removeClass('disabled');
    $preloadContainer.css("z-index", -999);
}

$( "#data-form" ).submit(function( event ) {
    console.log("SUBMIT");
    event.preventDefault();
    //disableWholeScreen();
    if (!abilityToChangePartOfFace){
        console.warn("In progress");
        return;
    }

    var sourceOfTheUserInputPhoto = $userInputPhoto.attr("src");
    if  (sourceOfTheUserInputPhoto == startInputPhoto){
        console.warn("No input Photo");
        return;
    }
    if (!activeExamplePhotoConfig.hasOwnProperty("faceId")){
        console.warn("No chosen example Face");
        return;
    }

    activeExamplePhotoConfig["activePartOfFace"] = activePartOfFace;
    activeExamplePhotoConfig["inputPhoto"] =  sourceOfTheUserInputPhoto;

    $.post( '/change_part_of_face/', activeExamplePhotoConfig).done(function(msg) {
        console.log("DONE");
        console.log("DONE");
        console.log("DONE");
        console.log("DONE");
        console.log(msg);
        if (msg["face_detected_successfully"]){
           console.log("SUCESS");
           console.log("SUCESS");
           console.log(msg);

           $chosenPartOfFace.attr('src',"");
           $chosenPartOfFace.attr('src', msg["img_src"]);
        }else {
            console.log(msg);
        }
        //console.log(typeof msg["face_detected_successfully"]);
    }).fail(function(msg){

    }).always(function () {
         abilityToChangePartOfFace = true;
    })
    }
);