import * as React from 'react'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/system'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Box from '@mui/material/Box'
import { theme } from './utils/style'

import Menu from './components/App/Menu'
import Footer from './components/App/Footer'

import Home from './pages/Home/'
import Error from './components/Error'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ pl: 1 }}>
        <Menu />
      </Box>
      <Box component="main" flex={1}>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="*" element={<Error />} />
          </Routes>
        </Router>
      </Box>
      <Footer />
    </ThemeProvider>
  )
}
