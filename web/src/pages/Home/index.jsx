import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Grid from '@mui/material/Grid'

import NavBar from '../../components/App/NavBar'
import Banner from '../../components/Home/Banner'
import InputQueryGenAI from '../../components/Home/InputQueryGenAI'
import GenAIResult from '../../components/Home/GenAIResult'
import TopSearches from '../../components/Home/TopSearches'
import TopSources from '../../components/Home/TopSources'
import LongProgress from '../../components/atoms/LongProgress'

import { useFetchGenAI } from '../../utils/hooks'

export default function Home() {
  const [displayQueryGenAI, setDisplayQueryGenAI] = React.useState(false)
  const [queryGenAI, setQueryGenAI] = React.useState()

  const onQueryGenAI = (query) => {
    setDisplayQueryGenAI(true)
    setQueryGenAI(query)
  }
  const { resultGenAI, isLoadingResultGenAI, errorLoadingResultGenAI } =
    useFetchGenAI(queryGenAI)

  return (
    <Stack spacing={2}>
      <NavBar selected="ask" />
      <Banner />
      <InputQueryGenAI onQueryGenAI={onQueryGenAI} />
      <Box sx={{pl:1}}>
      {!displayQueryGenAI ? null : errorLoadingResultGenAI ? (
        <span>Impossible to generate the content</span>
      ) : isLoadingResultGenAI ? (
        <LongProgress message="Generating ..." />
      ) : (
        <GenAIResult resultGenAI={resultGenAI} />
      )}
      </Box>
      <Grid container spacing={1} sx={{ pr: 1 }} alignItems="stretch">
        <Grid item sm={12} md={6}>
          <TopSearches />
        </Grid>
        <Grid item sm={12} md={6}>
          <TopSources />
        </Grid>
      </Grid>
    </Stack>
  )
}
