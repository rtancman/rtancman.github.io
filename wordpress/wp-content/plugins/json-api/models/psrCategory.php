<?php

class JSON_API_PsrCategory extends JSON_API_Category {
  
  var $type;        // String
  
  function import_wp_object($wp_category) {
    parent::import_wp_object($wp_category);
    $this->type =  get_field('categoria_tipo', 'category_' . $this->id);
  }

}

?>
