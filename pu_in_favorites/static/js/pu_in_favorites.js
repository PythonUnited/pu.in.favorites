// pu_in namespace
if (pu_in == undefined) {
  var pu_in = {};
}


// Our own namespace
pu_in['favorites'] = {};


/**
 * Add folder on back-end. Insert resulting html into list.
 */
pu_in.favorites.folderAdded = function() {

  $("#pu_in_favorites_add_folder_form").hide();
             
  var folder = $("#favorites_admin .favoritesfolder").last();

  $("#pu_in_favorites_add_folder_form input[name='_title']").val("");
  
  folder.find('.favorites').sortable({
      connectWith: '.favorites',
        delay: 100,
        revert: true,
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        update: pu_in.favorites.sort_favorite_update
        });
  
  if ($(".favoritesfolder").size() > 7) {
    $("#add_favoritesfolder").hide();
  }
  
  $(document).triggerHandler("pu_in_favorites_add_folder", [folder]);
};


/**
 * Edit folder and update folder html with result.
 */
pu_in.favorites.edit_favoritesfolder = function(id, data, reload) {

  $.post("/favorites/edit/favoritesfolder/" + id,
         data,
         function(response) {
           if (response['status'] != 0) {
             pg.showMessage(response['errors'], "error");
           } else {
             if (reload) {
               $("#favoritesfolder_" + id).replaceWith(response['html']);
               $(document).triggerHandler("pu_in_favorites_update_folder", 
                                          [$("#favoritesfolder_" + id)]);
             }
           }
         });  
};


/**
 * Update favorite.
 */
pu_in.favorites.edit_favorite = function(id, data, reload) {

  $.post("/favorites/edit/favorite/" + id,
         data,
         function(response) {
           if (response['status'] != 0) {
             pg.showMessage(response['errors'], "error");
           } else {
             if (reload) {
               $("#favorite_" + id).replaceWith(response['html']);
               $(document).triggerHandler("pu_in_favorites_update_favorite", 
                                          [$("#favorite_" + id)]);

             }
           }
         });  
};


/**
 * Bind events for favorites. Do this as 'delegate' events on the document.
 */
pu_in.favorites.bind_events = function() {

  $("body").on("click", ".favorite_action", function(e) {
      return pu_in.favorites.handle_favorite_action($(e.target));
    });

  $("body").on("click", ".editable form .cancel", function(e) {
      $(e.target).parents("form").hide();
      $(e.target).parents(".editable").removeClass("edit");
      e.preventDefault();
    });

  $("#pu_in_favorites_add_folder_form .cancel").click(function(e) {
      $("#pu_in_favorites_add_folder_form").hide();
      e.preventDefault();
    });

  $("body").on("click", ".toggle", function(e) {
      $(e.target).parents(".favoritesfolder").toggleClass("expanded");
      e.preventDefault();
    });

  $("body").on("submit", ".form-inline", function(e) {

      var form = $(e.target);
      var tgt = form.attr("target");

      $.post(form.attr("action"),
             form.serialize(),
             function(data, status, xhr) {
               
               if (data['status'] != 0) {
                 pg.showMessage(data['errors'], "error");
               } else {
                 $(tgt).replaceWith(data['html']);
                 if ($(tgt).hasClass("favoritesfolder")) {
                   $(document).triggerHandler("pu_in_favorites_update_folder", 
                                              [$(tgt)]);
                 } else {
                   $(document).triggerHandler("pu_in_favorites_update_favorite", 
                                              [$(tgt)]);
                 }
               }                 
             });

      e.stopPropagation();
      e.preventDefault();
    });
};


/**
 * Show add button if less than 8 left.
 */
pu_in.favorites.folderdeleted = function() {

  if ($(".favoritesfolder").size() < 8) {
    $("#add_favoritesfolder").show();
  }
};


/**
 * Sorting update handle.
 * @param event Event that triggered this function
 * @param ui Object that has been moved
 */
pu_in.favorites.sort_favoritesfolder_update = function(event, ui) {

  var data = {};
  var row_id = ui.item.attr("id");
  var item_id = row_id.substr(16);

  data['order'] = ui.item.parents(".sortable").eq(0).sortable("toArray").indexOf(row_id);

  pu_in.favorites.edit_favoritesfolder(item_id, data, false);
};


/**
 * Sorting update handle.
 * @param event Event that triggered this function
 * @param ui Object that has been moved
 */
pu_in.favorites.sort_favorite_update = function(event, ui) {

  var folder = ui.item.parents(".favoritesfolder").eq(0).attr("id").substr(16);
  var data = {};
  var row_id = ui.item.attr("id");
  var item_id = row_id.substr(9);

  if (this === ui.item.parent()[0]) {
    if (ui.sender) {
      data['folder'] = folder;
    }
    
    data['order'] = ui.item.parents("ol").eq(0).sortable("toArray").indexOf(row_id);
    
    pu_in.favorites.edit_favorite(item_id, data, false);
  }
};


$(document).ready(function() {
    
    pu_in.favorites.bind_events();
 
    //Making the favorite folders sort- and draggable
    $('#favorites_admin').sortable({
        handle: "header",
        delay: 100,
        revert: true,
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        update: pu_in.favorites.sort_favoritesfolder_update
      });

    $('.favorites').sortable({
        connectWith: '.favorites',
        delay: 100,
        revert: true,
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        update: pu_in.favorites.sort_favorite_update
        });

  });
