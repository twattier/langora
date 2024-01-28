import { createTheme } from '@mui/material/styles'
import { indigo } from '@mui/material/colors';

export const layout = {
  bannerHeight: 100,
}

export const colors = {
  light: '#efefef',
  dark: '#a9a9a9',
}

let theme = createTheme({
  palette: {
    primary: indigo,
    secondary: {
      main: '#ff383f',
    },
    background: {
      default: '#efefef',
    },
    text: {
      primary: '#000000',
    },
    dark: {
      main: "#a9a9a9",
      contrastText: "#fff",
    }
  },
})

theme = createTheme(theme, {  
  components: {
    MuiBox: {
      styleOverrides: {
        root: {
          borderRadius: 1,
          borderColor: theme.palette.dark.main, //notworking
        },
      },
    },
  },
})
export default theme
