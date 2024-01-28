import * as React from 'react'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Box from '@mui/material/Box'
import { layout } from './utils/style'
import theme from './utils/style'

import Menu from './components/Menu'
import Footer from './components/Footer'

import Home from './pages/Home/'
import Error from './components/Error'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Menu />
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
