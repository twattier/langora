import * as React from 'react'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Box from '@mui/material/Box'
import { theme, layout } from './utils/style'

// import Menu from './components/Menu'
// import Header from './components/Header'

import Home from './pages/Home/'
import Error from './components/Error'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: layout.bannerHeight }}>Menu</Box>
      <Box component="main" flex={1} bgcolor={'#eaeff1'}>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />            
            <Route path="*" element={<Error />} />
          </Routes>
        </Router>
      </Box>
    </ThemeProvider>
  )
};
