This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/import?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

## Configure Prettier on VS Code (i.e how to autoformat your code on saving)

Second, install Prettier as VS Code extension. Once you have installed it, you can use it with CTRL + CMD + P (MacOS) or CTRL + Shift + P (Windows) to manually format a file or a selection of code. You should have an opened file to perform it. If you don’t want to format your file manually every time, you can format it on save as well. Therefore you need to open your Visual Studio Code User's settings/preferences as JSON and put in the following configuration:

```
// Set the default
"editor.formatOnSave": false,
// Enable per-language
"[javascript]": {
"editor.formatOnSave": true
}
```

If you open up the VS Code User's settings/preferences as UI, search for "Format On Save" and make sure to activate it. Afterward, the file should format automatically once you save it. Now you don’t need to worry about your code formatting anymore, because Prettier takes care of it. You and your team can follow one code format.
