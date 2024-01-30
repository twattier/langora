import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'

import { ContentBox } from '../../utils/style/component'
import ListItemSearch from '../atoms/ListItemSearch'
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
          <Typography
            variant="subtitle1"
            align="center"
            color="primary"
            sx={{ fontWeight: 'bold' }}
          >
            Top Searches
          </Typography>
          <Divider />
          {topSearches?.map((search) => (       
             <ListItemSearch search={search} />
          ))}
        </Stack>
      )}
    </ContentBox>
  )
}
