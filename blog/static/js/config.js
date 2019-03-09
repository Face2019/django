var $userInputPhoto = $("[data-user-input-photo]");

var numberOfModalPhotos = null;
var modalPhotoIndex = null;
var modalPartOfFace = null;

var activePartOfFace = "lips";
var $acitveExampleFaces = $("[data-example-part-of-face=" + activePartOfFace + "]");
var numberOfExampleFaces = $acitveExampleFaces.find("[data-example-face]").length;
var activeExamplePhotoConfig = {};
var exampleFacexIndex = 0;

var $buttonPartOfFace = $("[data-part-of-face]");
var downloadedPartsOfFace = {
    "lips": true,
    "nose": false
};

var $chooseExamplFace = $("[data-choose-example-face]");
var $imagesShowingExampleFaces = $("[data-face-id]");

var $body = $("body");

var $preloadContainer = $("[data-loading-container]");

var $nextFace = $("[data-next-face]");
var $previousFace = $("[data-prev-face]");
var $chosenPartOfFace = $("[data-chosen-example-face]");

var LOAD_FACES_URL = "/load_faces/";

var $exampleFacesDiv = $("[data-example-faces]");

var defaultImageSourceOfTheChosenFace = $chosenPartOfFace.attr('src');

var startInputPhoto = $userInputPhoto.attr('src');
var abilityToChangePartOfFace = true;

//var $zoomPhoto =  $("[data-zoom]");
var $modalWithExampleFace = $("[data-chose-example-face-modal]");