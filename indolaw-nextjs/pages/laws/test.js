import remark from 'remark'
import html from 'remark-html'
import matter from 'gray-matter'
import fs from 'fs'
import path from 'path'

export default function Test(props) {
return (
  <>
    <h1>Test Page for rendering Markdown</h1>
    <div dangerouslySetInnerHTML={{ __html: props.data.contentHtml }}></div>
  </>)
}

export async function getStaticProps() {
  const markdownDirectory = ''
  const fullPath = path.join(markdownDirectory, `pre-rendering.md`)
  const fileContents = fs.readFileSync(fullPath, 'utf8')

  // Use gray-matter to parse the post metadata section
  const matterResult = matter(fileContents)

  // Use remark to convert markdown into HTML string
  const processedContent = await remark()
    .use(html)
    .process(matterResult.content)
  const contentHtml = processedContent.toString()

  return {
    props: {
      data: {
        contentHtml,
        ...matterResult.data
      }
    }
  }
}
