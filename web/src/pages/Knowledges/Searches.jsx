import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/Sources/NavBar'

export default function Searches() {
  return (
    <Stack>
      <NavBar selected="searches"/>
      <ContentBox>SEARCHES</ContentBox>
    </Stack>
  )
}
