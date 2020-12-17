# Youtube comment clustering 

This is a project for rearranging youtube comment.\
You can use the service in the following link : https://wltn0029.github.io/comment-clustering/ 

## Downloading model checkpoint
For model checkpoint for english, please download `checkpoint.pt` from:
```
https://drive.google.com/file/d/1WGX3CkiJMv7l5OM0_RM2NOxN2FD5T2GY/view?usp=sharing
```
and put `checkpoint.pt` inside `backend/model/` directory.
For model checkpoint for korean, please download 'kor\_model.pt' from:
```
https://drive.google.com/file/d/1hxghxWqEoXWdOu7fCFtDco9Ji50D6E4T/view?usp=sharing
```
and put `kor\_model.pt' inside `backend/model/` directory.

## Available Scripts

In the react directory (`./react`), you can run:

### `yarn start`

Runs the service in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn build`

Builds the service for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

To deploy on your own git hub page, fix the content of  `homepage` in the `./react/package.json`

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

