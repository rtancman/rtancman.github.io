<?php

class JSON_API_PsrAuthor extends JSON_API_Author {
  
  var $login;                  // String
  var $email;                  // String
  var $caps;                   // Array
  var $roles;                  // Array
  var $allcaps;                // Array
  var $user_registered;        // string
  var $user_meta;       // string
  
  function JSON_API_PsrAuthor($wp_author = null) {
    if ($wp_author) {
      $this->import_wp_object($wp_author);
    }
  }

  function import_wp_object($wp_author) {
    
    $this->id = (int) $wp_author->id;
    $this->slug = $wp_author->slug;
    $this->name = $wp_author->display_name;
    $this->description = $wp_author->description;
    $this->nickname = $wp_author->user_nicename;
    $this->url = $wp_author->user_url;
    
    //novos
    $this->login = $wp_author->user_login;
    $this->email = $wp_author->user_email;
    $this->caps = $wp_author->caps;
    $this->roles = $wp_author->roles;
    $this->allcaps = $wp_author->allcaps;
    $this->user_registered = $wp_author->user_registered;
    $this->user_meta = get_user_meta($this->id);
  }
  
}

?>
