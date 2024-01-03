import './Header.css';
import Text from './Text.jsx';
import Button from './Button.jsx';

function Header() {
  return (
    <div className='main-header-div'>
      <header>
        <Text />
        <Button />
      </header>
    </div>
  )
}

export default Header;