<?php
/*
Controller name: Authors
Controller description: Data manipulation methods for posts
*/

class JSON_API_Authors_Controller {

  protected function get_author_object($wp_author) {
    if (!$wp_author) {
      return null;
    }
    return new JSON_API_PsrAuthor($wp_author);
  }

  protected function list_authors($args = null) {
    //return wp_list_authors($args);
    return get_users($args);
  }

  public function get_authors() {
    $arr = array();
    $args = array(
      'who' => 'contributor',
      'orderby' => 'ID',
    );
    foreach ($this->list_authors($args) as $key) {
      array_push($arr, $this->get_author_object($key));
    }
    return array(
      'count' => count($arr),
      'list' => $arr
    );
  }

  public function get_author_id() {
    global $json_api;
    $arr = array();
    $args = array(
      'who' => 'contributor',
      'orderby' => 'ID',
    );
    if($json_api->query->author_id){
      $args['search'] = $json_api->query->author_id;
    }
    foreach ($this->list_authors($args) as $key) {
      $arr = $this->get_author_object($key);
      break;
    }
    return array(
      'author' => $arr
    );
  }

}

?>
