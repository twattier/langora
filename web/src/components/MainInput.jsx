import { useTheme } from '@mui/material/styles'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import InputAdornment from '@mui/material/InputAdornment'
import IconButton from '@mui/material/IconButton'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
import SearchIcon from '@mui/icons-material/Search'

export default function MainInput() {
  const theme = useTheme()

  return (
    <Stack
      direction="row"
      spacing={2}      
      // bgcolor={`${theme.palette.dark}`}
    >
      <TextField
        fullWidth
        multiline
        id="mainInput"        
        InputProps={{
          endAdornment: (
            <InputAdornment>
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />
      <IconButton
        sx={{ pl: 2, pr: 2 }}
        color="secondary"
      >
        <AutoAwesomeIcon />
      </IconButton>
    </Stack>
  )
}
