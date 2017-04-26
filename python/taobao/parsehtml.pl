#!/usr/bin/perl 
use HTML::Element; 
use HTML::TreeBuilder; 
use HTML::Parser; 
  
foreach my $file_name (@ARGV) { 
    my $root = HTML::TreeBuilder->new; 
    $root->parse_file($file_name); 
    $body=$root->find_by_tag_name('body'); 
    $p=$body->find_by_attribute('lang','es-MX');　　##在当前节点及其子节点下寻找lang属性为es-MX的节点 
    print $p->as_text(); 
    print "\n"; 
    $tree = $root->delete; 
} 

