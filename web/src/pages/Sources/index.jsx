import * as React from 'react'
import Stack from '@mui/material/Stack'
import Grid from '@mui/material/Grid'

import Banner from '../../components/Home/Banner'
import QueryInput from '../../components/Home/InputQueryGenAI'
import LongProgress from '../../components/atoms/LongProgress'
import SimilaritiesResults from '../../components/SimilaritiesResults'
import GenAIResult from '../../components/Home/GenAIResult'
import TopSearches from '../../components/Home/TopSearches'
import TopSources from '../../components/Home/TopSources'

import { useFetchSimilarities, useFetchGenAI } from '../../utils/hooks'

export default function Home() {
  const [displayQuerySearch, setDisplayQuerySearch] = React.useState(false)
  const [displayQueryGenAI, setDisplayQueryGenAI] = React.useState(false)
  const [querySearch, setQuerySearch] = React.useState()
  const [queryGenAI, setQueryGenAI] = React.useState()

  const onQuerySearch = (query) => {
    setDisplayQuerySearch(true)
    setDisplayQueryGenAI(false)
    setQuerySearch(query)
  }
  const { similarities, isLoadingSimilarities, errorLoadingSimilarities } =
    useFetchSimilarities(querySearch)

  const onQueryGenAI = (query) => {
    setDisplayQuerySearch(false)
    setDisplayQueryGenAI(true)
    alert("'" + query + "'")
    setQueryGenAI(query)
  }
  const { resultGenAI, isLoadingResultGenAI, errorLoadingResultGenAI } =
    useFetchGenAI(queryGenAI)

  return (
    <Stack spacing={2}>
      <Banner />
      <QueryInput onQuerySearch={onQuerySearch} onQueryGenAI={onQueryGenAI} />

      {!displayQuerySearch ? null : errorLoadingSimilarities ? (
        <span>Impossible to the retrieve similarities</span>
      ) : isLoadingSimilarities ? (
        <LongProgress message="Seeking similarities ..." />
      ) : (
        <SimilaritiesResults similarities={similarities} />
      )}

      {!displayQueryGenAI ? null : errorLoadingResultGenAI ? (
        <span>Impossible to generate the content</span>
      ) : isLoadingResultGenAI ? (
        <LongProgress message="Generating ..." />
      ) : (
        <GenAIResult resultGenAI={resultGenAI} />
      )}

      <Grid container spacing={1} sx={{pr:1}} alignItems="stretch">
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
