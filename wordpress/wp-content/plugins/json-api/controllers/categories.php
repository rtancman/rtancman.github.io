<?php
/*
Controller name: Categories
Controller description: Data manipulation methods for posts
*/

class JSON_API_Categories_Controller {

  protected function get_category_object($wp_category) {
    if (!$wp_category) {
      return null;
    }
    return new JSON_API_PsrCategory($wp_category);
  }

  protected function list_categories($args = null) {
    global $json_api;
    return get_categories($args);
  }

  public function get_categories() {
    $arr = array();
    $args = array(
      'hide_empty' => 0,
      'orderby' => 'term_group',
    );
    foreach ($this->list_categories($args) as $key) {
      array_push($arr, $this->get_category_object($key));
    }
    return array(
      'count' => count($arr),
      'categories' => $arr
    );
  }

  public function get_categories_types() {
    global $json_api;
    $arr = array();
    $args = array(
      'hide_empty' => 0,
      'orderby' => 'term_group',
    );

    if($json_api->query->father){
      $args['parent'] = 0;
    }
    
    foreach ($this->list_categories($args) as $key) {
      $category = $this->get_category_object($key);
      if($category->type){
        $arr[$category->type][] = $category;
      }else{
        $arr['default'][] = $category;
      }
    }
    return $arr;
  }
  
  public function get_categories_author() {
  }

  public function get_menu() {
    $menu = wp_get_nav_menu_items('area-da-vida');
    return $menu;
  }
  
}

?>
