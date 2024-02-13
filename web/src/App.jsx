import * as React from 'react'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/system'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Box from '@mui/material/Box'
import { theme } from './utils/style'

import Footer from './components/App/Footer'

import Home from './pages/Home/'

import Topics from './pages/Knowledges/Topics'
import Searches from './pages/Knowledges/Searches'
import Sources from './pages/Knowledges/Sources'
import Tasks from './pages/Knowledges/Tasks'

import Error from './components/Error'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* <Box sx={{ pl: 1 }}>
        <Menu />
      </Box> */}
      <Box component="main" flex={1}>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/knowledges" element={<Topics />} />
            <Route path="/knowledges/topics" element={<Topics />} />
            <Route path="/knowledges/searches" element={<Searches />} />
            <Route path="/knowledges/searches/:searchId" element={<Searches />} />
            <Route path="/knowledges/sources" element={<Sources />} />
            <Route path="/knowledges/sources/:sourceId" element={<Sources />} />
            <Route path="/knowledges/tasks" element={<Tasks />} />
            <Route path="*" element={<Error />} />
          </Routes>
        </Router>
      </Box>
      <Footer />
    </ThemeProvider>
  )
}
