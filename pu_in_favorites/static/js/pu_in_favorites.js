
// pu_in namespace
if (pu_in == undefined) {
  var pu_in = {};
}

// Our own namespace
pu_in['favorites'] = {};

pu_in.favorites.show_add_folder = function() {
  $("#pu_in_favorites_add_folder_form").show();
};

pu_in.favorites.add_folder = function() {

  var form = $("#pu_in_favorites_add_folder_form form");

  $.post("/favorites/favorites",
         form.serialize() + "&action=add_folder",
         function(data) {
           alert(data['message']);
           $("#pu_in_favorites_add_folder_form").hide();
         });

};
