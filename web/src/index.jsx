import React from 'react'
import Container  from '@mui/material/Container'

import {createRoot} from 'react-dom/client'
import reportWebVitals from './reportWebVitals'
import App from './App'

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Container maxWidth="lg">
      <App sx={{ bgcolor: '#cfe8fc'}}/>
    </Container>
  </React.StrictMode>
);
reportWebVitals();