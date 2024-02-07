import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/App/NavBar'

export default function Sources() {
  return (
    <Stack>
      <NavBar selected="sources"/>
      <ContentBox>SOURCES</ContentBox>
    </Stack>
  )
}
