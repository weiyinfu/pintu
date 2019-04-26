package weidiao.pintu;

import android.app.Activity;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Random;

public class MainActivity extends Activity {
    class MyView extends View {
        public MyView(Context context) {
            super(context);
            init();
            shuffle();
            initPaint();
        }

        final int width = 4, height = 6;
        int a[][] = new int[width][height];
        Point last;
        Point space;
        int d[] = {-1, 0, 0, -1, 1, 0, 0, 1};
        Paint fill, stroke;

        @Override
        public boolean onTouchEvent(MotionEvent event) {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                last = new Point((int) event.getX(), (int) event.getY());
            } else if (event.getAction() == MotionEvent.ACTION_UP) {
                double dx = event.getX() - last.x, dy = event.getY() - last.y;
                double the = Math.atan2(dy, dx);
                if (the < 0) the += Math.PI * 2;
                int min = 0;
                for (int i = 1; i < 4; i++) {
                    if (Math.abs(the - min * Math.PI / 2) > Math.abs(the - i * Math.PI / 2)) {
                        min = i;
                    }
                }
                if (move(min)) {
                    if (isWin()) {
                        Toast.makeText(getContext(), "you win!", Toast.LENGTH_LONG).show();
                        init();
                        shuffle();
                    }
                    postInvalidate();
                }
            }
            return true;
        }

        void initPaint() {
            fill = new Paint();
            fill.setColor(Color.BLACK);
            fill.setStyle(Paint.Style.FILL);
            stroke = new Paint();
            stroke.setTextSize(60);
            stroke.setStrokeWidth(3);
            stroke.setStyle(Paint.Style.STROKE);
            stroke.setColor(Color.WHITE);
        }

        void init() {
            for (int i = 0; i < width; i++) {
                for (int j = 0; j < height; j++) {
                    a[i][j] =j* width + i+1;
                }
            }
            a[width-1][height-1]=0;
            space = new Point(width-1, height-1);
        }

        boolean move(int dir) {
            int x = space.x + d[dir << 1], y = space.y + d[dir << 1 | 1];
            if (x < 0 || x >= width || y < 0 || y >= height) return false;
            a[space.x][space.y] = a[x][y];
            a[x][y] = 0;
            space = new Point(x, y);
            return true;
        }

        void shuffle() {
            Random r = new Random();
            for (int i = 0; i < 100; i++) {
                move(r.nextInt(4));
            }
        }

        boolean isWin() {
            int all = width * height;
            for (int i = 0; i < width; i++) {
                for (int j = 0; j < height; j++) {
                    if (a[i][j] != (j*width+i+1) % all) {
                        return false;
                    }
                }
            }
            return true;
        }

        @Override
        protected void onDraw(Canvas canvas) {
            float w = Math.min(getWidth() / width, getHeight() / height);
            for (int i = 0; i < width; i++) {
                for (int j = 0; j < height; j++) {
                    canvas.drawRect(i * w + 2, j * w + 2, i * w + w - 2, j * w + w - 2, fill);
                    if (a[i][j] > 0)
                        canvas.drawText(a[i][j] + "", i * w + 102, j * w + 102, stroke);
                }
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(new MyView(this));
    }
}