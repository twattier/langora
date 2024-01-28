import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'

import Banner from '../../components/Banner'
import MainInput from '../../components/MainInput'
import TopSearches from '../../components/TopSearches'
import TopSources from '../../components/TopSources'

export default function Home() {
  return (
    <Stack spacing={2}>
      <Banner />
      <MainInput />
      <Box flex={1}>Result</Box>
      <Stack direction="row" spacing={2}>
        <TopSearches />
        <TopSources />
      </Stack>
    </Stack>
  )
}
