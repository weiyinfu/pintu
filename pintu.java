import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.MenuBar;
import java.awt.Rectangle;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.geom.Rectangle2D;
import java.awt.image.BufferedImage;
 
import javax.swing.*;
 
import java.util.Random; 
 
import javax.swing.*;
 
public class Pintu extends JFrame {
    public static void main(String []args) {
        new Pintu();
    }
 
    int[][] a = new int[4][4];
    int x, y;
 
    void init() {
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++)
                a[i][j] = i * 4 + j;
        x=y=3;
    }
 
    Pintu() {
        setTitle("拼图游戏-made by weidiao.neu");
        setSize(600,600);
        addKeyListener(listenKey);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
        init();
        shuffle();
    }
    @Override
    public void paint(Graphics g) {
        Container pane=getContentPane();
        BufferedImage bit=new BufferedImage(pane.getWidth(),pane.getHeight(),BufferedImage.TYPE_INT_ARGB);
        Graphics gg=bit.getGraphics();
        gg.setColor(Color.BLUE);
        gg.fillRect(0, 0, bit.getWidth(), bit.getHeight());
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
                if(a[i][j]==15)continue;
                gg.drawImage(getPic(a[i][j]), j*pane.getWidth()/4, i*pane.getHeight()/4, pane.getWidth()/4-1, pane.getHeight()/4-1, null);
            }
        }
        pane.getGraphics().drawImage(bit, 0, 0, null);
    }
    private BufferedImage getPic(int i) {
        BufferedImage bit;
        Font font=new Font("Consolas",Font.BOLD,50);
        Rectangle2D rec= getFontMetrics(font).getStringBounds(i+"", getGraphics());
        bit=new BufferedImage((int)rec.getWidth(),(int)rec.getHeight(),BufferedImage.TYPE_INT_ARGB);
        Graphics gg=bit.getGraphics();
        gg.setColor(Color.BLACK);
        gg.fillRect(0, 0, bit.getWidth(), bit.getHeight());
        gg.setFont(font);
        gg.setColor(Color.RED);
        gg.drawString(i+"",0, getFontMetrics(font).getAscent());
        return bit;
    }
 
    private void shuffle() {
        Random r=new Random();
        for(int i=0;i<100;i++){
            int p=r.nextInt(15);
            int q=r.nextInt(15);
            if(p==q){
                i--;
            }
            else{
                int temp=a[p/4][p%4];
                a[p/4][p%4]=a[q/4][q%4];
                a[q/4][q%4]=temp;
            }
        }
    }
 
    KeyListener listenKey = new KeyAdapter() {
 
        @Override
        public void keyReleased(KeyEvent e) {
            switch (e.getKeyCode()) {
            case KeyEvent.VK_UP:
                if (x == 3)
                    return;
                else {
                    int temp = a[x][y];
                    a[x][y] = a[x + 1][y];
                    a[x + 1][y] = temp;
                    x++;
                }
                break;
            case KeyEvent.VK_DOWN:
                if (x == 0)
                    return;
                else {
                    int temp = a[x][y];
                    a[x][y] = a[x - 1][y];
                    a[x - 1][y] = temp;
                    x--;
                }
                break;
            case KeyEvent.VK_RIGHT:
                if (y == 0)
                    return;
                else {
                    int temp = a[x][y];
                    a[x][y] = a[x][y - 1];
                    a[x][y - 1] = temp;
                    y--;
                }
                break;
            case KeyEvent.VK_LEFT:
                if (y == 3)
                    return;
                else {
                    int temp = a[x][y];
                    a[x][y] = a[x][y + 1];
                    a[x][y + 1] = temp;
                    y++;
                }
                break;
            }
            repaint();
            if(checkWin()){
                JOptionPane.showMessageDialog(Pintu.this, "You win");
                init();
                shuffle();
                repaint();
            }
        }
 
        private boolean checkWin() {
            // TODO Auto-generated method stub
            for(int i=0;i<4;i++)
                for(int j=0;j<4;j++)
                    if(a[i][j]!=i*4+j)
                        return false;
            return true;
        }
    };
}