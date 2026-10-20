# 回归检查：论文标题、作者和属性中的特殊字符应作为文本展示。
require 'liquid'

source = File.read(File.expand_path('../_includes/lab/publication.html', __dir__))
paper = {
  'title' => 'Performance of <GPU> kernels & "I/O"',
  'year' => 2026, 'topic' => 'hpc', 'venue' => 'Research & Systems',
  'volume' => '1', 'issue' => nil, 'pages' => '1-2',
  'doi' => '10.example/test', 'source' => 'https://example.org/?a=1&b="two"',
  'authors' => ['Jianjiang Li', 'A & B'],
  'summary' => {'zh' => '文本包含 <tag> & 引号', 'en' => 'A <tag> & text'}
}
html = Liquid::Template.parse(source).render!(
  'include' => {'pub' => paper, 'summary' => true}, 'lang' => 'en',
  't' => {'publisher_link' => 'Publisher', 'topics' => {'hpc' => 'HPC'}}
)
expectations = [
  html.include?('Performance of &lt;GPU&gt; kernels &amp; &quot;I/O&quot;'),
  html.include?('A &amp; B'),
  html.include?('<strong>Jianjiang Li</strong>'),
  html.include?('a=1&amp;b=&quot;two&quot;'),
  !html.include?('<GPU>'), !html.include?('<tag>')
]
abort 'HTML 特殊字符转义回归失败。' unless expectations.all?
puts 'HTML 特殊字符转义：6 项检查通过。'
