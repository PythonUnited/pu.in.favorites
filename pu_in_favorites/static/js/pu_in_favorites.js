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
 * Show edit folder form.
 */
pu_in.favorites.show_edit_folder_form = function(folder_title, folder_id) {

  var form = $("#pu_in_favorites_edit_folder_" + folder_id);

  form.show();
  form.next().hide();
};


/**
 * Show edit favorite form.
 */
pu_in.favorites.show_favorite_edit_form = function(event) {
  
  var tgt = $(event.target);
  var row = tgt.parents(".content_item").eq(0);
  var form = row.find(".pu_in_favorites_edit_form").eq(0);

  form.show();
  form.next().hide();

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
             $("#favorites").append(data['html']);
             pu_in.favorites.rebind_events();
           }
           
         });
};


/**
 * Edit folder and update folder html with result.
 */
pu_in.favorites.edit_folder = function() {

  var form = $("#pu_in_favorites_edit_folder_form form");
  var folder_id = form.find(":input[name='id']").val();

  $.post("/favorites/edit/favoritesfolder/" + folder_id,
         form.serialize(),
         function(data) {

           if (data['status'] != 0) {
             pg.showMessage(data['errors'], "error");
           } else {
             $("#pu_in_favorites_edit_folder_form").hide();             
             $("#favoritesfolder_" + folder_id).replace(data['html']);
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
             tgt.parents(".content_item").eq(0).remove(data['html']);
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
      
      $(this).click(pu_in.favorites.delete);

    });

  elt.find(".json-edit").each(function() {
      
      if (rebind) {
        $(this).unbind("click");
      }
      
      $(this).click(pu_in.favorites.show_favorite_edit_form);

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
  
  $(".content_item").each(function() {
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


$(document).ready(function() {

    $(".pu_in_favorites_edit_folder_form .cancel").click(function() {
        var form = $(this).parents(".pu_in_favorites_edit_folder_form");
        form.hide();
        form.next().show();        
      });

    $(".favorite_action").click(function() {
        return pu_in.favorites.handle_favorite_action($(this));
      });
    
    $(".content_item").each(function() {
        pu_in.favorites.bind_events($(this), true);
      });
     
  });