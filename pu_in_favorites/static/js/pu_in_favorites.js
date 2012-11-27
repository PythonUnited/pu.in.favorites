// pu_in namespace
if (pu_in == undefined) {
  var pu_in = {};
}


// TODO: move to core module
pu_in['core'] = {};

pu_in.core.formatErrors = function(dict) {

  var errors = "<dl>";

  for (key in dict) {
    errors += "<dt>" + key + "</dt><dd>" + dict[key] + "</dd>";
  }

  return errors + "</dl>";
};

// Our own namespace
pu_in['favorites'] = {};


/**
 * Show the add folder form.
 */
pu_in.favorites.show_add_folder = function() {

  $("#pu_in_favorites_add_folder_form input[name='_title']").val("");
  $("#pu_in_favorites_add_folder_form").show();
};


/**
 * Show edit form.
 */
pu_in.favorites.show_edit_form = function(tgt) {

  tgt.parents(".editable").eq(0).addClass("edit");
};


/**
 * Add folder on back-end. Insert resulting html into list.
 */
pu_in.favorites.add_folder = function() {

  var form = $("#pu_in_favorites_add_folder_form form");

  $.post("/favorites/add/favoritesfolder",
         form.serialize(),
         function(data) {
           
           if (data['status'] != 0) {
             pg.showMessage(data['errors'], "error");
           } else {             
             $("#pu_in_favorites_add_folder_form").hide();
             $("#favorites_admin").append(data['html']);
             
             var folder = $("#favorites_admin .favoritesfolder").last();

             folder.find('.favorites').sortable({
                 connectWith: '.favorites',
                   delay: 100,
                   revert: true,
                   placeholder: "placeholder",
                   forcePlaceholderSize: true,
                   update: pu_in.favorites.sort_favorite_update
                   });
             
             if ($("li.favoritesfolder").size() > 7) {
               $("#add_favoritesfolder").hide();
             }

             $(document).triggerHandler("pu_in_favorites_add_folder", [folder]);
           }           
         });
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
             }
           }
         });  
};


/**
 * Delete folder and remove html from list.
 */
pu_in.favorites.delete_item = function(event) {
  
  var tgt = $(event.target);

  if (tgt.context.nodeName != "A") {
    tgt = tgt.parents("a").eq(0);
  }

  $.post(tgt.attr("href"),
         {},
         function(data) {
           
           if (data['status'] != 0) {
             pg.showMessage(data['errors'], "error");
           } else {
             tgt.parents(".editable").eq(0).remove();
           }
         });

  event.stopPropagation();
  event.preventDefault();
};


/**
 * Bind events for favorites. Do this as 'delegate' events on the document.
 */
pu_in.favorites.bind_events = function() {

  $("body").on("click", ".favorite_action", function(e) {
      return pu_in.favorites.handle_favorite_action($(e.target));
    });

  $("body").on("click", ".edit form .cancel", function(e) {
      $(e.target).parents(".editable").eq(0).removeClass("edit");      
      e.preventDefault();
    });

  $("body").on("click", ".toggle", function(e) {
      $(e.target).parents(".favoritesfolder").find("ol").toggle("slow");
      $(e.target).parents(".favoritesfolder").toggleClass("expanded");
      e.preventDefault();
    });

  $("body").on("click", ".json-rm", function(e) {

      pg.confirmMessage("Weet je zeker dat je dit item wilt verwijderen?", pu_in.favorites.delete_item, [e]);
      e.preventDefault();
    });

  $("body").on("click", ".json-edit", function(e) {
      
      pu_in.favorites.show_edit_form($(e.target));
      e.preventDefault();
    });

  $("body").on("submit", ".form-inline", function(e) {

      var form = $(e.target);
      var tgt = form.attr("target");

      $.post(form.attr("action"),
             form.serialize(),
             function(data) {
               
               if (data['status'] != 0) {
                 pg.showMessage(data['errors'], "error");
               } else {
                 $(tgt).replaceWith(data['html']);
               }                 
             });
      return false;
    });
};


/**
 * Handle the favorite action button.
 * @param action Action link/button.
 */
pu_in.favorites.handle_favorite_action = function(action) {

  var tgt = action.attr("target");

  $.post(action.attr("href"),
         action.attr("pu:action-data"),
         function(data) {
           if (data['status'] != 0) {
             pg.showMessage(pu_in.core.formatErrors(data['errors']), "error");
           } else {
             if (tgt) {
               $(tgt).html(data['html']);
             } else {
               console.log("replace");
               console.log(action);
               action.replaceWith(data['html']);
             }
           }
         },
         "json");
  
  return false;
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
