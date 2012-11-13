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
pu_in.favorites.show_edit_form = function(event) {

  var tgt = $(event.target);

  tgt.parents("li").eq(0).addClass("edit");

  event.stopPropagation();
  event.preventDefault();
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
             pu_in.favorites.rebind_events();
           }
           
         });
};


/**
 * Edit folder and update folder html with result.
 */
pu_in.favorites.edit_favoritesfolder = function(id, data) {

  $.post("/favorites/edit/favoritesfolder/" + id,
         data,
         function(response) {
           if (response['status'] != 0) {
             pg.showMessage(response['errors'], "error");
           } else {
             $("#favoritesfolder_" + id).replaceWith(response['html']);
           }
         });  
};


/**
 * Update favorite.
 */
pu_in.favorites.edit_favorite = function(id, data) {

  $.post("/favorites/edit/favorite/" + id,
         data,
         function(response) {
           if (response['status'] != 0) {
             pg.showMessage(response['errors'], "error");
           } else {
             $("#favorite_" + id).replaceWith(response['html']);
           }
         });  
};


/**
 * Delete folder and remove html from list.
 */
pu_in.favorites.delete = function(event) {
  
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
             tgt.parents("li").eq(0).remove();
           }
         });

  event.stopPropagation();
  event.preventDefault();
};


/**
 * Bind events to element.
 * @param elt Element to do
 * @param rebind Whether to unbind first
 */
pu_in.favorites.bind_events = function(elt, rebind) {
  
  elt.find(".json-rm").each(function() {
      
      if (rebind) {
        $(this).unbind("click");
      }
      
      $(this).click(
                    function(e) {
                      pg.confirmMessage("Weet u zeker dat u dit item wilt verwijderen?", pu_in.favorites.delete, [e]);
                      e.preventDefault();
                    });
    });

  elt.find(".json-edit").each(function() {
      
      if (rebind) {
        $(this).unbind("click");
      }
      
      $(this).click(pu_in.favorites.show_edit_form);
    });

  elt.find("form").each(function() {

      if (rebind) {
        $(this).unbind("submit");
      }
      
      $(this).submit(function() {

          var tgt = $(this).attr("target");

          $.post($(this).attr("action"),
                 $(this).serialize(),
                 function(data) {
                   
                   if (data['status'] != 0) {
                     pg.showMessage(data['errors'], "error");
                   } else {
                     $(tgt).replaceWith(data['html']);
                     pu_in.favorites.bind_events($(tgt), true);
                   }                 
                 });
          return false;
        });
    });
};


/**
 * Renew all event handlers.
 */
pu_in.favorites.rebind_events = function() {
  
  $(".favorite,.favoritesfolder").each(function() {
      pu_in.favorites.bind_events($(this), true);
    });
};


pu_in.favorites.handle_favorite_action = function(action) {

  var tgt = action.attr("target");

  $.post(action.attr("href"),
         action.attr("pu:action-data"),
         function(data) {
           if (data['status'] != 0) {
             pg.showMessage(pu_in.core.formatErrors(data['errors']), "error");
           } else {
             if (tgt) {

               var parent = $(tgt).parent();

               $(tgt).replaceWith(data['html']);
               parent.find(".favorite_action").click(function() {
                   return pu_in.favorites.handle_favorite_action($(this));
                 });
             } else {
               var parent = action.parent();

               action.replaceWith(data['html']);
               parent.find(".favorite_action").click(function() {
                   return pu_in.favorites.handle_favorite_action($(this));
                 });
             }
           }
         });
  
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

  data['order'] = ui.item.parents("ol").eq(0).sortable("toArray").indexOf(row_id);
  pu_in.favorites.edit_favoritesfolder(item_id, data);
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
    
    pu_in.favorites.edit_favorite(item_id, data);
  }
};


$(document).ready(function() {

    $(".pu_in_favorites_edit_folder_form .cancel").click(function() {
        var form = $(this).parents(".pu_in_favorites_edit_folder_form");
        form.hide();
        form.next().show();        
      });

    $(".favorite_action").click(function() {
        return pu_in.favorites.handle_favorite_action($(this));
      });
    
    $("#favorites_admin li").each(function() {
        pu_in.favorites.bind_events($(this), true);
      });
 
    //Making the favorite folders sort- and draggable
    $('#favorites_admin').sortable({
        revert: false,
        delay: 150,
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        update: pu_in.favorites.sort_favoritesfolder_update
      });

    $('#xfavorites_admin').draggable({
        revert: "invalid",
          snap: true,
          });
    
    // Making the favorite items sort- and draggable
    $('.favorites').sortable({
        connectWith: '.favorites',
        delay: 150,
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        update: pu_in.favorites.sort_favorite_update
        });

  });
