import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'

import { ContentBox, ContentBoxTitle } from '../../utils/style/component'
import ListSearches from '../atoms/ListSearches'
import { useFetchTopSearches } from '../../utils/hooks'

export default function TopSearches() {
  const { topSearches, isLoadingTopSearches, errorLoadingTopSearches } =
    useFetchTopSearches()
  if (errorLoadingTopSearches) {
    return <span>Impossible to load the liste of Searches</span>
  }

  return (
    <ContentBox sx={{ width: '100%' }}>
      {isLoadingTopSearches ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1} sx={{ m: 1 }}>
          <ContentBoxTitle>Top Searches</ContentBoxTitle>
          <Divider />
          <ListSearches searches={topSearches} />
        </Stack>
      )}
    </ContentBox>
  )
}
