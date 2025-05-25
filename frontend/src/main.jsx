import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import MainRouter from './routes/MainRouter.jsx'
import {Provider} from "react-redux"
import store from './components/store.js'

createRoot(document.getElementById('root')).render(
     <Provider store={store}>
     <MainRouter/>
     </Provider>

)
