import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'


import ListItemSource from '../atoms/ListItemSource'
import { ContentBox } from '../../utils/style/component'
import { useFetchTopSources } from '../../utils/hooks'

export default function TopSources() {
  const { topSources, isLoadingTopSources, errorLoadingTopSources } =
    useFetchTopSources()
  if (errorLoadingTopSources) {
    return <span>Impossible to load the liste of sources</span>
  }

  return (
    <ContentBox sx={{ width: '100%' }}>
      {isLoadingTopSources ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1} sx={{ m: 1 }}>
          <Typography
            variant="subtitle1"
            align="center"
            color="primary"
            sx={{ fontWeight: 'bold' }}
          >
            Top Sources
          </Typography>
          <Divider />
          {topSources?.map((source) => (
            <ListItemSource source={source} />
          ))}
        </Stack>
      )}
    </ContentBox>
  )
}
