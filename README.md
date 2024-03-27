# Sports statistics measurement system

### Installation
Install dependencies from the repository directory:
1. **frontend**
```bash
$ npm install
```
2. **backend**
```bash
$ pip install -r requirements.txt
```

### Setup (development)
**To start everything together**:
```bash
$ npm start
```
**To run everything separately**:
1. Start frontend:
```bash
$ npm run parcel
```
2. Start backend:
```bash
$ flask --app server run
```

You can access the website on `http://localhost:1234`.

### Bulding (production)
```bash
$ npm build
```

### DO NOT UPLOAD `node_modules` NOR `dist` FOLDER NOR `.parcel-cache` NOR `__pycache__`!
